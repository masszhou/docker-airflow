import logging
import datetime
from pathlib import Path
from airflow import DAG
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator


from importROS import rosbag


LOGGER = logging.getLogger("airflow.task")


default_args = {
    "owner": "zhiliang zhou",
    "depends_on_past": False,
    "start_date": datetime.datetime(2021, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0
}


def parse_rosbag(rosbag_path: Path, 
                 save_root: Path, 
                 **kwargs):
    reader = rosbag.RosbagReader(rosbag_path)

    save_lanecamera = rosbag.SaveToLocal(topic_name="/camera/lane_detector",
                                         root_path=save_root,
                                         date_folder=Path("2020-06-18-12-45-06"),
                                         sensor_folder=Path("lane_camera"),
                                         ext=".png")
    save_velodyne = rosbag.SaveToLocal(topic_name="/velodyne_points",
                                       root_path=save_root,
                                       date_folder=Path("2020-06-18-12-45-06"),
                                       sensor_folder=Path("velodyne"),
                                       ext=".npy")
    save_scala1 = rosbag.SaveToLocal(topic_name="/scala1/pointcloud",
                                     root_path=save_root,
                                     date_folder=Path("2020-06-18-12-45-06"),
                                     sensor_folder=Path("scala1"),
                                     ext=".npy")
    save_scala2 = rosbag.SaveToLocal(topic_name="/scala2/pointcloud",
                                     root_path=save_root,
                                     date_folder=Path("2020-06-18-12-45-06"),
                                     sensor_folder=Path("scala2"),
                                     ext=".npy")
    save_scala3 = rosbag.SaveToLocal(topic_name="/scala3/pointcloud",
                                     root_path=save_root,
                                     date_folder=Path("2020-06-18-12-45-06"),
                                     sensor_folder=Path("scala3"),
                                     ext=".npy")
    save_scala4 = rosbag.SaveToLocal(topic_name="/scala4/pointcloud",
                                     root_path=save_root,
                                     date_folder=Path("2020-06-18-12-45-06"),
                                     sensor_folder=Path("scala4"),
                                     ext=".npy")
    save_to_local = (save_lanecamera, save_velodyne, save_scala1, save_scala2, save_scala3, save_scala4)

    upload_to_mongodb = rosbag.UploadToMongoDB(save_to_local)
    for each in reader.next():
        upload_to_mongodb(*each)


dag = DAG("upload_rosbag_daily", default_args=default_args, schedule_interval="@once")
with dag:

    dummy_start_up = DummyOperator(task_id='All_jobs_start')
    dummy_shut_down = DummyOperator(task_id='All_jobs_end')

    file_name = "2020-06-18-12-45-06.bag"
    upload_rosbag_op = PythonOperator(
        task_id=f"parse-and-upload-{file_name}-into-DB",
        python_callable=parse_rosbag,
        provide_context=True,
        op_kwargs={
            'rosbag_path': Path("/data/rosbag_daily/2020-06-18-12-45-06.bag"),
            'save_root': Path("/data/rosbag_daily/"),
            },
    )

    dummy_start_up >> upload_rosbag_op >> dummy_shut_down