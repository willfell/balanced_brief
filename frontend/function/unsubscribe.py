import boto3
import os
import json
from dbmanage import *
from swag_functions import *


def unsubscribe_user(event, context):
    # CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": True,
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS, DELETE",
    }

    # Check if this is an OPTIONS request (CORS preflight)
    if event["httpMethod"] == "OPTIONS":
        return {"statusCode": 204, "headers": headers, "body": None}
    
    print("the method was NOT options")

    # Check if this is a POST request
    if event["httpMethod"] == "DELETE":
        print(json.dumps(event))
        requestor = json.loads(event["body"]) if event["body"] else {}
        print(json.dumps(requestor, indent=4))
        success, response = check_user_and_unsubscribe(requestor['email'])
        if success:
            return {
                "statusCode": 201,
                "headers": headers,
                "body": json.dumps(response),
            }
        else:
            return {
                "statusCode": 409,
                "headers": headers,
                "body": json.dumps(response),
            }

    return {
        "statusCode": 405,
        "headers": headers,
        "body": json.dumps(response),
    }
