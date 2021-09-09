from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2021, 4, 5),
    'email': ['nemes.dan123@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'cluj_imobiliare_dag',
    default_args=default_args,
    description='Web scraper for real estate information using website www.imobiliare.ro. Information saved into csv file'
                'and then inserted into PostgreSQL database.',
    schedule_interval=timedelta(days=7),
)

run_webscrapper = BashOperator(
    task_id='web_scrapper_imobiliare',
    bash_command='python /home/dan/PycharmProjects/DissertationProject/imobiliare/scrapper_cluj_imobiliare.py',
    dag=dag)

run_processer = BashOperator(
    task_id='csv_processer',
    bash_command='python /home/dan/PycharmProjects/DissertationProject/processers/cluj_imobiliare_processer.py',
    dag=dag)

run_webscrapper >> run_processer

