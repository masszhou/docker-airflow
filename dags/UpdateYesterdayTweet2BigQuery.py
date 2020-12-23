from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator

import logging
import datetime
import twint

#directly import
# from sensors.gcs_bq_custom_sensor import GoogleCloudStorageBigQueryUpdateSensor
#using airflow plugin
from airflow.sensors import GoogleCloudStorageBigQueryUpdateSensor
from airflow.contrib.operators import gcs_to_bq
from google.cloud import storage
from google.oauth2 import service_account

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.datetime(2020, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

def scrapeYesterdayTwitter(bucket_name, project, credentials_path: str=None, **kwargs):
    """setting up the google credentials"""
    credentials = service_account.Credentials.from_service_account_file(credentials_path) if credentials_path else None
    storage_client = storage.Client(project=project, credentials=credentials)
    bucket = storage_client.bucket(bucket_name)

    #get_yesterday
    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
    #setting up twitter scraper
    tweetConfig = twint.Config()
    searchTerm = "coronavirus"
    tweetConfig.Search = searchTerm
    tweetConfig.Since = f"{yesterday.strftime('%Y-%m-%d')} 00:00:00"
    tweetConfig.Until = f"{datetime.datetime.today().strftime('%Y-%m-%d')} 00:00:00"
    tweetConfig.Lang = "en"
    tweetConfig.Verified = True
    #storing the result in the pandas dataframe
    tweetConfig.Pandas = True
    tweetConfig.Limit = 100
    tweetConfig.Stats = False
    tweetConfig.Hide_output = True

    twint.run.Search(tweetConfig)

    Tweets_df = twint.storage.panda.Tweets_df

    filename = f"tweet-{searchTerm}-{yesterday.strftime('%Y-%m-%d')}"

    bucket.blob('{}/{}.csv'.format("airflowTweet", filename)).upload_from_string(Tweets_df.to_csv(), 'text/csv')
    blob = bucket.get_blob('{}/{}.csv'.format("airflowTweet", filename))
    blob.metadata = {'updatedTime': datetime.datetime.now()}
    blob.patch()

    logging.info('{}/{}.csv has been uploaded.'.format("airflowTweet", filename))

def checkingYesterdayTweet(bucket_name, project, credentials_path, **kwargs):
    """
    If the data CSV file was saved, it triggers the All_jobs_end task; 
    else it set off the tweeter-today-scraper.
    """
    credentials = service_account.Credentials.from_service_account_file(credentials_path) if credentials_path else None

    storage_client = storage.Client(project=project, credentials=credentials)
    bucket_name = "storage-ark2"
    bucket = storage_client.get_bucket(bucket_name)
    yesterday = datetime.datetime.today() - datetime.timedelta(days=1)

    searchTerm = "coronavirus"
    filename = f"tweet-{searchTerm}-{yesterday.strftime('%Y-%m-%d')}"

    if bucket.blob(filename).exists():
        logging.info('this file exist: {}/{}.csv'.format("airflowTweet", filename))
        return "All_jobs_end"

    logging.info('this file does not exist: {}/{}.csv'.format("airflowTweet", filename))
    return "tweeter-yesterday-scraper"

dag = DAG('UpdateYesterdayTweet2BigQuery', default_args=default_args, schedule_interval="@daily", catchup=False)

with dag:
    check_modified_date_sensor = GoogleCloudStorageBigQueryUpdateSensor(
        task_id='check_modified_date_sensor',
        project='project-ark2',
        credentials_path='/usr/local/airflow/dags/project-ark2-b9b253cd02fa.json',
        timeout=60*60*24, # timeout in 1 day
        poke_interval=60*60*1, # checking files every 1 hours
    )

    GCS_to_BQ = gcs_to_bq.GoogleCloudStorageToBigQueryOperator(
        task_id='gcs_to_bq',
        bucket='storage-ark2',
        source_objects=['airflowTweet/*.csv'],
        destination_project_dataset_table='tweetScraper.tweet',
        skip_leading_rows=1,
        source_format='CSV',
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_TRUNCATE',
        bigquery_conn_id='google_cloud_default',
        allow_quoted_newlines=True, #allows for newlines
        allow_jagged_rows=True, #allows for missing values
        autodetect=True
    )

    dummy_shut_down = DummyOperator(
        task_id='All_jobs_end')

    checkingYesterdayTweet = BranchPythonOperator(
        task_id='branching',
        python_callable=checkingYesterdayTweet,
        op_kwargs={'bucket_name': 'storage-ark2', 
                   'project': 'project-ark2', 
                   'credentials_path': '/usr/local/airflow/dags/project-ark2-b9b253cd02fa.json'},
        provide_context=True)

    scrapeYesterdayData = PythonOperator(
        task_id="tweeter-yesterday-scraper",
        python_callable=scrapeYesterdayTwitter,
        provide_context=True,
        op_kwargs={'bucket_name': 'storage-ark2', 
                   'project': 'project-ark2', 
                   'credentials_path': '/usr/local/airflow/dags/project-ark2-b9b253cd02fa.json'},
    )

    [checkingYesterdayTweet, check_modified_date_sensor] >> GCS_to_BQ >> dummy_shut_down