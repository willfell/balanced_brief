import boto3
import os

INSTANCEID = os.environ['INSTANCEID']

def start_instance(event, context):
    ec2 = boto3.client('ec2')
    print(f"Attempting to start instance {INSTANCEID}")
    try:
        ec2.start_instances(InstanceIds=[INSTANCEID])
        print(f"Successfully started instance: {INSTANCEID}")
    except boto3.exceptions.botocore.exceptions.ClientError as e:
        print(f"Failed to start instance {INSTANCEID}. Error: {e}")

def stop_instance(event, context):
    ec2 = boto3.client('ec2')
    print(f"Attempting to stop instance {INSTANCEID}")
    try:
        ec2.stop_instances(InstanceIds=[INSTANCEID])
        print(f"Successfully stopped instance: {INSTANCEID}")
    except boto3.exceptions.botocore.exceptions.ClientError as e:
        print(f"Failed to stop instance {INSTANCEID}. Error: {e}")
