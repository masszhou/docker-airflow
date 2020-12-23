from datetime import timedelta, datetime
from airflow import DAG
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2020, 5, 9),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0
}

dag = DAG("TestGCS2BigQuery", default_args=default_args, schedule_interval="@once")

with dag:    
    gcs2bq_schema = GoogleCloudStorageToBigQueryOperator(
        task_id='test_gcs2bq',
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

    gcs2bq_schema
