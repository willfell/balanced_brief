import boto3
import os
import json


def add_user(event, context):
    print(event)
    # CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",  
        "Access-Control-Allow-Credentials": True,
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS, POST"
    }

    # Check if this is an OPTIONS request (CORS preflight)
    if event['httpMethod'] == 'OPTIONS':
        return {
            'statusCode': 204,
            'headers': headers,
            'body': None
        }
    
    # Check if this is a POST request
    if event['httpMethod'] == 'POST':
        # Process the POST request
        # Assuming body is JSON and not None
        body = json.loads(event['body']) if event['body'] else {}
        # Your business logic here...

        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({"result": "User signed up"})
        }

    # If we got here, the method is not allowed
    return {
        'statusCode': 405,
        'headers': headers,
        'body': json.dumps({"message": "Method Not Allowed"})
    }
