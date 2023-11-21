import boto3
import os
import json
from dbmanage import *
from swag_functions import *


def verify_user(event, context):
    # CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": True,
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS, PUT",
    }

    # Check if this is an OPTIONS request (CORS preflight)
    if event["httpMethod"] == "OPTIONS":
        return {"statusCode": 204, "headers": headers, "body": None}

    # Check if this is a POST request
    if event["httpMethod"] == "PUT":
        print(json.dumps(event))
        requestor = json.loads(event["body"]) if event["body"] else {}
        print(json.dumps(requestor, indent=4))
        verify_user = update_user_verification(requestor["email"])
        if verify_user:
            return {
                "statusCode": 201,
                "headers": headers,
                "body": json.dumps({"message": "User Verified"}),
            }
        else:
            return {
                "statusCode": 409,
                "headers": headers,
                "body": json.dumps({"message": "Failed to verify user"}),
            }

    return {
        "statusCode": 405,
        "headers": headers,
        "body": json.dumps({"message": "Method Not Allowed"}),
    }
