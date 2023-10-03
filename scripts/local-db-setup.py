import boto3
import os
import subprocess

def download_and_execute_file(bucket_name, key, download_path):
    # Initialize the S3 client
    s3 = boto3.client('s3')

    # Download the file from S3
    s3.download_file(bucket_name, key, download_path)

    # Execute the file
    subprocess.run(["/opt/homebrew/bin/python3", download_path])

if __name__ == "__main__":
    # Define S3 bucket details and download path
    bucket = 'balanced-brief-terraform-state'
    file_key = 'setup.py'
    local_path = 'setup.py'
    
    download_and_execute_file(bucket, file_key, local_path)
