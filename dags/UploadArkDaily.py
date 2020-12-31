from datetime import timedelta, datetime
from airflow import DAG
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
import logging
import datetime
from google.cloud import storage
from google.oauth2 import service_account
from typing import Tuple, Optional, List, Union
from pathlib import Path
import olefile
import pandas as pd
import uuid
import glob


default_args = {
    "owner": "zhiliang zhou",
    "depends_on_past": False,
    "start_date": datetime.datetime(2020, 12, 31),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0
}


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
            df = df.rename(columns={'% of ETF': 'PercentOfETF'})

    return df


def uploadLocalArkDailyToGCS(credentials_path: str,
                             project_id: str,
                             bucket_name: str):
    """setting up the google credentials"""
    credentials = service_account.Credentials.from_service_account_file(credentials_path) if credentials_path else None
    storage_client = storage.Client(project=project_id, credentials=credentials)
    bucket = storage_client.bucket(bucket_name)

    xls_path = glob.glob('/data/ark_daily/*.xls')  # path depends on docker-compose.yml

    for each_path in xls_path:
        df_ark = load_ark_xls(each_path)
        path = Path(each_path)

        filename = path.stem
        foldname = "ark_daily"
        gcs_file = f'{foldname}/{filename}.csv'

        if bucket.get_blob(gcs_file) is None:
            bucket.blob(gcs_file).upload_from_string(df_ark.to_csv(), 'text/csv')
        else:
            logging.info(f'this file exist: {gcs_file}')


dag = DAG("UploadArkDaily", default_args=default_args, schedule_interval="@daily")
with dag:
    upload_local_ark_daily_to_gcs = PythonOperator(
        task_id="upload-ark-daily-to-gcs",
        python_callable=uploadLocalArkDailyToGCS,
        provide_context=True,
        op_kwargs={
            'bucket_name': 'storage-ark2',
            'project': 'project-ark2',
            'credentials_path': '/usr/local/airflow/dags/project-ark2-b9b253cd02fa.json'
        },
    )

    upload_local_ark_daily_to_gcs
