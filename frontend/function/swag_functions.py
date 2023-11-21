import boto3
import json



def verify_user_job(event):
    lambda_client = boto3.client("lambda")
    lambda_client.invoke(
        FunctionName="user-signup-UserVerificationEmail-C8N4woAyuJQg",
        InvocationType="Event",  # Asynchronous invocation
        Payload=(json.dumps(event)),  # Pass event data to the other function
    )
