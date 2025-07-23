from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import boto3

def trigger_glue_job():
    glue = boto3.client('glue')
    glue.start_job_run(JobName='clean-transactions')

default_args = {
    'start_date': datetime(2023, 1, 1),
    'retries': 1
}

dag = DAG('ecommerce_pipeline', default_args=default_args, schedule_interval='@daily')

start = BashOperator(task_id='start_pipeline', bash_command='echo "Pipeline started."', dag=dag)

glue_task = PythonOperator(task_id='run_glue_job', python_callable=trigger_glue_job, dag=dag)

start >> glue_task