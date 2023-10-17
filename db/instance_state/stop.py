import os
import boto3

# Ensure that the instance is off

def stop_instance_and_wait(instance_id, region_name="us-west-1"):
    
    # Create an EC2 client
    ec2 = boto3.client('ec2', region_name=region_name)
    
    # Stop the instance
    ec2.stop_instances(InstanceIds=[instance_id])
    print(f"Stopping instance: {instance_id}")

    # Wait until the instance is stopped
    waiter = ec2.get_waiter('instance_stopped')
    waiter.wait(InstanceIds=[instance_id])
    
    print(f"Instance {instance_id} is now fully stopped.")

if os.environ['EXECUTION_LOCATION'] == 'CLOUD':
    stop_instance_and_wait('i-0e028110e871745fe')
