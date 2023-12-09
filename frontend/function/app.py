import boto3
import os
import json
from dbmanage import *
from swag_functions import *


def add_user(event, context):
    print(event)
    # CORS headers
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": True,
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS, POST",
    }

    # Check if this is an OPTIONS request (CORS preflight)
    if event["httpMethod"] == "OPTIONS":
        return {"statusCode": 204, "headers": headers, "body": None}

    # Check if this is a POST request
    if event["httpMethod"] == "POST":
        print(json.dumps(event))
        # Process the POST request
        # Assuming body is JSON and not None
        requestor = json.loads(event["body"]) if event["body"] else {}
        print(json.dumps(requestor, indent=4))
        user_duplicate = check_for_duplicate_user(requestor)
        if user_duplicate:
            return {
                "statusCode": 409,
                "headers": headers,
                "body": json.dumps({"message": "Duplicate user detected"}),
            }

        add_user = add_user_to_db(requestor)
        if add_user:
            print("Adding user successful kicking off verification email send")
            verify_user_job(event)
            return {
                "statusCode": 201,
                "headers": headers,
                "body": json.dumps({"message": "User successfully added"}),
            }
        else:
            return {
                "statusCode": 500,
                "headers": headers,
                "body": json.dumps({"message": "Internal Server Error"}),
            }

    # If we got here, the method is not allowed
    return {
        "statusCode": 405,
        "headers": headers,
        "body": json.dumps({"message": "Method Not Allowed"}),
    }
