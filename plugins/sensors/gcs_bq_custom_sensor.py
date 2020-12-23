from airflow.operators.sensors import BaseSensorOperator
from airflow.utils.decorators import apply_defaults
from google.cloud import bigquery
from google.cloud import storage
from google.oauth2 import service_account
import datetime

class GoogleCloudStorageBigQueryUpdateSensor(BaseSensorOperator):
    """
    See if the modified date of the big query dataset is less than modified date of the GCS files.
    """

    @apply_defaults
    def __init__(self,
                 project,
                 credentials_path,
                 *args, **kwargs):
        super(GoogleCloudStorageBigQueryUpdateSensor, self).__init__(*args, **kwargs)
        self.project = project
        self.credentials_path = credentials_path

    def poke(self, context):
        self.log.info('Sensor checks existence of objects: %s', self.project)
   
        credentials = service_account.Credentials.from_service_account_file(self.credentials_path) if self.credentials_path else None

        client = bigquery.Client(project=self.project, credentials=credentials)

        # dataset_id = 'your-project.your_dataset'

        dataset = client.get_dataset('tweetScraper')
        tables_list = list(client.list_tables(dataset))

        storage_client = storage.Client(project=self.project, credentials=credentials)
        bucket_name = "storage-ark2"
        bucket = storage_client.get_bucket(bucket_name)

        for table_item in tables_list:
            table = client.get_table(table_item.reference)

            self.log.info("Table {} last modified: {}".format(table.table_id, table.modified)) 
        
            for blob in bucket.list_blobs(prefix='airflowTweet/'):
                blob_object = bucket.get_blob(blob.name)

                lastUpdatedTime = datetime.datetime.strptime(blob_object.metadata['updatedTime']+" +0000", '%Y-%m-%d %H:%M:%S.%f %z')

                self.log.info("Bucket Metadate : %s" % (lastUpdatedTime))

                if(lastUpdatedTime > table.modified):
                    self.log.info("is this file older than last modififed: %s " % (lastUpdatedTime > table.modified))
                    return True

            return False