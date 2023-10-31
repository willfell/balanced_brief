import os
import boto3
import psycopg2
import time
# Ensure that the instance is on
DB_PASS = os.environ['POSTGRES_DB_PASS']
DB_HOST = os.environ['POSTGRES_DB_HOST']
DB_USER = 'db_user'
DB_NAME = 'postgres'
DB_PORT = '5432'

def connect_to_db(retry_times=60, delay=5):
    for _ in range(retry_times):
        try:
            connection = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASS)
            print("Successfully connected to the database!")
            return connection
        except psycopg2.OperationalError as e:
            print(f"Failed to connect to the database. Retrying in {delay} seconds. Error: {e}")
            time.sleep(delay)
    raise Exception("Failed to connect to the database after multiple attempts.")



def start_instance_and_wait(instance_id, region_name="us-west-1"):
    # Create an EC2 client
    ec2 = boto3.client('ec2', region_name=region_name)
    
    # Start the instance
    ec2.start_instances(InstanceIds=[instance_id])
    print(f"Started instance: {instance_id}")

    # Wait until the instance is running
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])
    
    print(f"Instance {instance_id} is now active.")

    

if os.environ['EXECUTION_LOCATION'] == 'CLOUD':
    start_instance_and_wait('i-0e028110e871745fe')
    connect_to_db()

