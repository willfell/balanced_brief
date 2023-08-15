import praw
import os
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import json
from functions import *
from datetime import datetime
import boto3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from premailer import transform


# Obtain the list of users
user_list = obtain_user_list()
post_list = obtain_posts()

email_list = determine_email_templates(user_list, post_list)

email_templates = create_email_templates(email_list)

email_list = retrieve_email_list()

# Your AWS credentials
region = 'us-west-1'  # e.g., 'us-west-2'

# Initialize SES client
client = boto3.client('ses', region_name=region)

# Create a MIME formatted message
msg = MIMEMultipart()
#msg['From'] = 'willfellhoelter@gmail.com'
msg['From'] = 'TheBalancedBrief@balancedbrief.com'
msg['Subject'] = 'The Balanced Brief'

# Read the HTML and CSS files
with open('newsletter/html/will_fell.html', 'r') as f:
    html_content = f.read()

with open('newsletter/html/email-template.css', 'r') as f:
    css_content = f.read()

# Combine the HTML and CSS
html_with_css = f"<style>{css_content}</style>" + html_content

# Inline the CSS
base_path = os.path.abspath('html/')
inlined_html = transform(html_with_css, base_url=f'file://{base_path}/')


# Attach the processed HTML with inlined CSS to the email
msg.attach(MIMEText(inlined_html, 'html'))

# Send the email
for user in email_list:
    print(f"Sending email to {user}")
    response = client.send_raw_email(
        Source=msg['From'],
        Destinations=[user],
        RawMessage={
            'Data': msg.as_string()
        }
    )

    print(response)
