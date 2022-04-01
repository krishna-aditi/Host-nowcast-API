# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 10:06:08 2022

@author: krish
"""

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import sys
from pathlib import Path
sys.path.append(os.path.join(Path.home(),'updatesevir'))
from nowcast_batch import batchrunAPI

def print_status():
    print('Successfully run Nowcast Cache Schedule Run')
    return 'Successfully run Nowcast Cache Schedule Run'
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email': ['airflow@airflow.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
  }

with DAG(dag_id='nowcast', default_args=default_args, schedule_interval='@hourly',catchup=False) as dag:
    

    # When running independently (For testing using API directly)
    t1 = PythonOperator(task_id='nowcast_cache',
                   python_callable=batchrunAPI)
    # Printing Status for debug
    t2 = PythonOperator(task_id='status_check',
                   python_callable=print_status)

    t1 >> t2
