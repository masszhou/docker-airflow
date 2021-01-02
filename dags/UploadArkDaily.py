import logging
from pathlib import Path
import pandas as pd
import uuid
import glob
import datetime

import olefile

from airflow import DAG
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator

from google.cloud import bigquery
from google.cloud import storage
from google.oauth2 import service_account

from typing import Tuple, Optional, List, Union


LOGGER = logging.getLogger("airflow.task")


default_args = {
    "owner": "zhiliang zhou",
    "depends_on_past": False,
    "start_date": datetime.datetime(2020, 12, 31),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0
}


def fix_exceptions(df: pd.DataFrame) -> pd.DataFrame:
    if '% Trade' in df.columns:
        # ARK_Trade_09082020.xls
        df = df.rename(columns={'% Trade': 'PercentOfETF'})
    return df


def load_ark_xls(path_str: str,
                 skiprows: Tuple = (0, 1, 2),
                 header: int = 0,
                 usecols: str = "A:H") -> Optional[pd.DataFrame]:
    """
    load ark xls file to pandas dataframe
    """
    df = None
    path = Path(path_str)
    check_list = path.stem.split("_")
    if "ARK" not in check_list or "Trade" not in check_list or path.suffix != ".xls":
        return df

    with open(path, 'rb') as file:
        ole = olefile.OleFileIO(file)
        if ole.exists('Workbook'):
            d = ole.openstream('Workbook')
            df = pd.read_excel(d, engine='xlrd', skiprows=skiprows, header=header, usecols=usecols)

            df["FUND"] = df["FUND"].astype('unicode')  # string or unicode type both works
            df["Date"] = pd.to_datetime(
                df['Date'],
                format='%Y-%m-%d',
                errors='coerce'
            )  # convert to datetime64[ns]
            df["Direction"] = df["Direction"].astype('unicode')
            df["Ticker"] = df["Ticker"].astype('unicode')
            df["CUSIP"] = df["CUSIP"].astype('unicode')
            df["Name"] = df["Name"].astype('unicode')
            # add UUID for database
            df['id'] = [uuid.uuid4().hex for _ in range(len(df.index))]
            df["id"] = df["id"].astype('unicode')
            # apply bigquery convention rule
            df = df.rename(columns={'% of ETF': 'PercentOfETF'})
            df = fix_exceptions(df)

    return df


def upload_to_bigquery(df: pd.DataFrame,
                       credentials_path: str,
                       project_id: str,
                       table_id: str):
    """
    direct upload and overwrite bigquery table with dataframe
    """
    credentials = service_account.Credentials.from_service_account_file(credentials_path) if credentials_path else None
    client = bigquery.Client(project=project_id, credentials=credentials)

    job_config = bigquery.LoadJobConfig(
        # Specify a (partial) schema. All columns are always written to the
        # table. The schema is used to assist in data type definitions.
        schema=[
            # Specify the type of columns whose type cannot be auto-detected. For
            # example the "title" column uses pandas dtype "object", so its
            # data type is ambiguous.
            bigquery.SchemaField("FUND", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField("Date", bigquery.enums.SqlTypeNames.DATE),  # convert datetime64[ns] to DATE type
            bigquery.SchemaField("Direction", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField("Ticker", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField("CUSIP", bigquery.enums.SqlTypeNames.STRING),
            bigquery.SchemaField("Name", bigquery.enums.SqlTypeNames.STRING),
            # bigquery.SchemaField("Shares", bigquery.enums.SqlTypeNames.INT64),
            # bigquery.SchemaField("PercentOfETF", bigquery.enums.SqlTypeNames.FLOAT64),
            bigquery.SchemaField("id", bigquery.enums.SqlTypeNames.STRING),
        ],
        # Optionally, set the write disposition. BigQuery appends loaded rows
        # to an existing table by default, but with WRITE_TRUNCATE write
        # disposition it replaces the table with the loaded data.
        write_disposition="WRITE_APPEND",  # WRITE_TRUNCATE = overwrite, WRITE_APPEND = append
    )

    job = client.load_table_from_dataframe(
        df, table_id, job_config=job_config
    )  # Make an API request.
    job.result()  # Wait for the job to complete.
    LOGGER.info(f'{df.shape[0]} rows appended to BigQuery  <{table_id}> in project <{project_id}>')


def upload_ark_daily(xls_path: str,
                     credentials_path: str,
                     project_id: str,
                     bucket_name: str,
                     table_id: str,
                     **kwargs):
    local_path = Path(xls_path)
    filename = local_path.stem

    # check if this xls file already existed in GCS
    cur_gcs_files = kwargs['ti'].xcom_pull(task_ids='check-ark-daily-gcs')
    if filename in cur_gcs_files:
        LOGGER.info(f'{filename} exist in GCS: <{bucket_name}>')
        return

    """setting up the google credentials"""
    credentials = service_account.Credentials.from_service_account_file(credentials_path) if credentials_path else None
    storage_client = storage.Client(project=project_id, credentials=credentials)
    bucket = storage_client.bucket(bucket_name)

    df_ark = load_ark_xls(xls_path)

    gcs_foldname = "ark_daily"
    gcs_file = f'{gcs_foldname}/{filename}.csv'

    bucket.blob(gcs_file).upload_from_string(df_ark.to_csv(), 'text/csv')
    LOGGER.info(f'{gcs_file} uploaded to GCS <{bucket_name}> in project <{project_id}>')
    upload_to_bigquery(df_ark, credentials_path, project_id, table_id)


def check_ark_daily_gcs(credentials_path: str,
                        project_id: str,
                        bucket_name: str,
                        **kwargs):
    credentials = service_account.Credentials.from_service_account_file(credentials_path) if credentials_path else None
    storage_client = storage.Client(project=project_id, credentials=credentials)
    bucket = storage_client.bucket(bucket_name)

    gcs_files = [Path(blob.name).stem for blob in storage_client.list_blobs(bucket_name, prefix='ark_daily')]
    # each.name -> ARK_Trade_12012020_0645PM_EST_5fc6baeab72df
    
    # Pushes gcs_files to XCom pool without a specific target, just by returning it
    # pulled_value_2 = kwargs['ti'].xcom_pull(task_ids='check-ark-daily-gcs')
    return gcs_files


def create_upload_ark_dag(dag_id, xls_path, dag):
    return PythonOperator(
        task_id=dag_id,
        python_callable=upload_ark_daily,
        provide_context=True,
        op_kwargs={
            'xls_path': xls_path,
            'credentials_path': '/usr/local/airflow/dags/project-ark2-b9b253cd02fa.json',
            'project_id': 'project-ark2',
            'bucket_name': 'storage-ark2',
            'table_id': 'stock.ark_daily',},
        dag=dag
    )


dag = DAG("upload_ark_daily", default_args=default_args, schedule_interval="@daily")
with dag:

    dummy_start_up = DummyOperator(task_id='All_jobs_start')
    dummy_shut_down = DummyOperator(task_id='All_jobs_end')

    check_ark_daily_gcs_op = PythonOperator(
        task_id="check-ark-daily-gcs",
        python_callable=check_ark_daily_gcs,
        provide_context=True,
        op_kwargs={
            'credentials_path': '/usr/local/airflow/dags/project-ark2-b9b253cd02fa.json',
            'project_id': 'project-ark2', 
            'bucket_name': 'storage-ark2', 
            },
    )

    local_xls = glob.glob('/data/ark_daily/*.xls')  # path depends on docker-compose.yml
    dag_ops = []
    for each in local_xls:
        dag_name = f"task-upload-{Path(each).stem}"
        # run all dags parallel
        # problem: Exceeded rate limits in BQ: too many table update operations for this table. 
        # dummy_start_up >> create_uoload_ark_dag(dag_name, each, dag) >> dummy_shut_down  
        dag_ops.append(create_upload_ark_dag(dag_name, each, dag))

    # run dag one by one, to avoid Exceeded rate limits in BigQuery
    # can be optimized with running by chunks
    # Problem: with increasing more CSV files, this sequential ops could be not efficent
    dummy_start_up >> check_ark_daily_gcs_op
    if len(dag_ops) == 1:
        check_ark_daily_gcs_op >> dag_ops[0]
    elif len(dag_ops) > 1:
        check_ark_daily_gcs_op >> dag_ops[0]
        for i in range(len(dag_ops)-1):
            dag_ops[i].set_downstream(dag_ops[i+1])
    dag_ops[-1] >> dummy_shut_down
