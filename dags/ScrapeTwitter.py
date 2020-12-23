from airflow import DAG
from google.cloud import storage
from google.oauth2 import service_account
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from io import BytesIO, StringIO

import pandas as pd
import numpy as np
import datetime
import logging
from dateutil.relativedelta import relativedelta

import twint

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.datetime(2020, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0
}

def scrapeTwitter(start_date, end_date, bucket_name, project, credentials_path: str=None, **kwargs):
    """setting up the google credentials"""
    credentials = service_account.Credentials.from_service_account_file(credentials_path) if credentials_path else None
    storage_client = storage.Client(project=project, credentials=credentials)
    bucket = storage_client.bucket(bucket_name)

    #setting up twitter scraper
    tweetConfig = twint.Config()

    searchTerm = "coronavirus"

    tweetConfig.Search = searchTerm
    tweetConfig.Since = start_date.strftime('%Y-%m-%d 00:00:00')
    tweetConfig.Until = end_date.strftime('%Y-%m-%d 00:00:00')
    tweetConfig.Lang = "en"
    tweetConfig.Verified = True
    #storing the result in the pandas dataframe
    tweetConfig.Pandas = True
    tweetConfig.Limit = 100
    tweetConfig.Stats = False
    tweetConfig.Hide_output = True

    twint.run.Search(tweetConfig)

    Tweets_df = twint.storage.panda.Tweets_df

    month = start_date.strftime("%b")

    filename = f"tweet-{searchTerm}-{month}"

    bucket.blob('{}/{}.csv'.format("airflowTweet", filename)).upload_from_string(Tweets_df.to_csv(), 'text/csv')
    blob = bucket.get_blob('{}/{}.csv'.format("airflowTweet", filename))
    blob.metadata = {'updatedTime': datetime.datetime.now()}
    blob.patch()

    logging.info('{}/{}.csv has been uploaded.'.format("airflowTweet", filename))

def createTwitterDag(start_date, dag_id, dag):

    end_date = start_date+relativedelta(months=1)

    return PythonOperator(
        task_id=dag_id,
        python_callable=scrapeTwitter,
        provide_context=True,
        op_kwargs={'start_date': start_date, 
                   'end_date': end_date, 
                   'bucket_name': 'storage-ark2', 
                   'project': 'project-ark2', 
                   'credentials_path': '/usr/local/airflow/dags/project-ark2-b9b253cd02fa.json'},
        dag=dag
    )

dag = DAG('ScrapeTwitter',default_args=default_args,catchup=False)

#I will do monthly
start_date = datetime.datetime(2020, 1, 1)
end_date = datetime.datetime.now()

with dag:
    #I will do monthly
    dummy_start_up = DummyOperator(
        task_id='All_jobs_start')
    
    dummy_shut_down = DummyOperator(
        task_id='All_jobs_end')
    #get the month difference between the two dates so we can create a monthly scraper.
    num_months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

    for n in range(num_months+1):
        dag_name = f"tweeter-{start_date.strftime('%B')}"
    
        dummy_start_up >> createTwitterDag(start_date, dag_name, dag) >> dummy_shut_down

        start_date = start_date+relativedelta(months=1)