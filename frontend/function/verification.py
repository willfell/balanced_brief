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

region='us-west-1'
client = boto3.client("ses", region_name=region)


def send_verification_email(event, context):
    print(event)    
    requestor = json.loads(event["body"]) if event["body"] else {}
    print(json.dumps(requestor, indent=4))
    print(requestor)
    recipient_email = requestor['email']

    with open('html/index.html', 'r') as file:
        html_content = file.read()

    html_content = html_content.replace("REPLACE_EMAIL_HERE", recipient_email)
    # Create a MIME message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Email Verification - Balanced Brief"
    msg['From'] = 'verification@balancedbrief.com'  
    msg['To'] = recipient_email

    # Attach the HTML content
    msg.attach(MIMEText(html_content, 'html'))
    # with open("html/email-template.css", "r") as f:
    #     css_content = f.read()

    # Combine the HTML and CSS
    # html_with_css = f"<style>{css_content}</style>" + html_content

    # Inline the CSS
    # base_path = os.path.abspath("html/")
    #cssutils.log.setLevel(logging.CRITICAL)
    # inlined_html = transform(html_with_css, base_url=f"file://{base_path}/")

    # Attach the processed HTML with inlined CSS to the email
    # msg.attach(MIMEText(inlined_html, "html"))
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

