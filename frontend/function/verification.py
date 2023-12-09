import boto3
import os
import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
from functools import wraps
import sys
import cssutils
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from premailer import transform

region = "us-west-1"
client = boto3.client("ses", region_name=region)


def send_verification_email(event, context):
    requestor = json.loads(event["body"]) if event["body"] else {}
    recipient_email = requestor["email"]

    with open("html/index.html", "r") as file:
        html_content = file.read()

    html_content = html_content.replace("REPLACE_EMAIL_HERE", recipient_email)
    # Create a MIME message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Email Verification - Balanced Brief"
    msg["From"] = "BalancedBriefVerification@balancedbrief.com"
    msg["To"] = recipient_email

    # Attach the HTML content
    msg.attach(MIMEText(html_content, "html"))
    response = None
    # Send the email
    print(f"Attempting to send email to {recipient_email}")
    try:
        response = client.send_raw_email(
            Source=msg["From"],
            Destinations=[recipient_email],
            RawMessage={"Data": msg.as_string()},
        )
        print(response)

    except Exception as e:
        print(e)

    print(response)
    return response
