from airflow.plugins_manager import AirflowPlugin
from sensors.gcs_bq_custom_sensor import GoogleCloudStorageBigQueryUpdateSensor

class AirflowCustomPlugin(AirflowPlugin):
    name = "airflow_custom_plugin"
    sensors = [GoogleCloudStorageBigQueryUpdateSensor]
    operators = []
    executors = []
    macros = []
    admin_views = []
    flask_blueprints = []
    menu_links = []