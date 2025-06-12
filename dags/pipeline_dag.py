from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import sys

# Добавляем корень проекта в sys.path для импорта etl-модулей
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)

from etl.extract import main as extract_main
from etl.transform import main as transform_main
from etl.train import main as train_main
from etl.evaluate import main as evaluate_main
from etl.upload import main as upload_main

# Параметры по умолчанию для тасков
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2025, 6, 12),
    'email_on_failure': False,
    'email_on_retry': False
}

dag = DAG(
    'pipeline_dag',
    default_args=default_args,
    description='ETL-пайплайн для диагностики заболеваний',
    schedule_interval='@daily',
    catchup=False
)

config_path = os.path.join(PROJECT_DIR, 'config.yaml')

extract = PythonOperator(
    task_id='extract',
    python_callable=extract_main,
    op_kwargs={'config_path': config_path},
    dag=dag
)

transform = PythonOperator(
    task_id='transform',
    python_callable=transform_main,
    op_kwargs={'config_path': config_path},
    dag=dag
)

train = PythonOperator(
    task_id='train',
    python_callable=train_main,
    op_kwargs={'config_path': config_path},
    dag=dag
)

evaluate = PythonOperator(
    task_id='evaluate',
    python_callable=evaluate_main,
    op_kwargs={'config_path': config_path},
    dag=dag
)

upload = PythonOperator(
    task_id='upload',
    python_callable=upload_main,
    op_kwargs={'config_path': config_path},
    dag=dag
)

extract >> transform >> train >> evaluate >> upload