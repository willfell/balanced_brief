import praw
import os
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import json
from functions import *
from datetime import datetime
import boto3
import logging
from functools import wraps
import sys
import cssutils

current_date = datetime.utcnow().strftime("%Y-%m-%d")

log = logging.getLogger()


# Obtain the list of users
user_list = obtain_user_list()
post_list = obtain_posts()
# email_list = determine_email_templates(user_list, post_list)
category_order_mapping = determine_category_order()

for user in user_list["list"]:
    print("====================================================================")
    print(f"Creating email template for user {user['user_email']}")
    print("====================================================================")
    user_newsletter = generate_newsletter(
        post_list, category_order_mapping, user, current_date
    )
    create_and_send_email(user_newsletter, user, current_date)
