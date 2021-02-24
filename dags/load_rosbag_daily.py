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

from typing import Tuple, Optional, List, Union, Optional
import rosbag

LOGGER = logging.getLogger("airflow.task")


default_args = {
    "owner": "zhiliang zhou",
    "depends_on_past": False,
    "start_date": datetime.datetime(2021, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 0
}


def extract_chunks(file_in: Path, 
                   chunks_size: int,  # Mb 
                   chunks_save_path: Optional[Path], 
                   **kwargs):
    if chunks_save_path is None:
        chunks_save_path = file_in.parent / file_in.stem  # new folder with the same stem name in the same folder
        chunks_save_path.mkdir(parents=True, exist_ok=True)  # be careful for permission
    chunks: int = file_in.stat().st_size/1000000//chunks_size

    bagfile = rosbag.Bag(file_in)
    messages = bagfile.get_message_count()
    m_per_chunk = int(round(float(messages) / float(chunks)))
    chunk = 0
    m = 0
    save_path = chunks_save_path / f"chunk_{chunk:04d}.bag"  # pad zeros for 4 digits
    outbag = rosbag.Bag(save_path, 'w')
    for topic, msg, t in bagfile.read_messages():
        m += 1
        if m % m_per_chunk == 0:
            outbag.close()
            chunk += 1
            save_path = chunks_save_path / f"chunk_{chunk:04d}.bag"  # pad zeros for 4 digits
            outbag = rosbag.Bag(save_path, 'w')
        outbag.write(topic, msg, t)
    outbag.close()
    LOGGER.info(f'split rosbag into {chunks+1} chunks done')



dag = DAG("upload_rosbag_daily", default_args=default_args, schedule_interval="@once")
with dag:

    dummy_start_up = DummyOperator(task_id='All_jobs_start')
    dummy_shut_down = DummyOperator(task_id='All_jobs_end')

    file_name = "2020-06-18-12-45-06.bag"
    split_rosbag_op = PythonOperator(
        task_id=f"split-{file_name}-into-chunks",
        python_callable=extract_chunks,
        provide_context=True,
        op_kwargs={
            'file_in': Path('/passat/2020-06-18-12-45-06.bag'),
            'chunks_size': 200, 
            'chunks_save_path': Path('/data/rosbag_daily'), 
            },
    )

    dummy_start_up >> split_rosbag_op >> dummy_shut_down