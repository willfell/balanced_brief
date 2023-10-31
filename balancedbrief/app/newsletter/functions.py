import os
import psycopg2
import json
from newspaper import Article
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from premailer import transform
import cssutils
import boto3
import logging

log = logging.getLogger()  

html_dir = 'html'

region = 'us-west-1'  
client = boto3.client('ses', region_name=region)

# set up connection parameters
db_pass = os.environ['POSTGRES_DB_PASS']
db_host = os.environ['POSTGRES_DB_HOST']
conn_params = {
    'host': db_host,
    'port': '5432',
    'database': 'postgres',
    'user': 'db_user',
    'password': db_pass
}

# Create a new connection and cursor object
conn = psycopg2.connect(**conn_params)
cur = conn.cursor()


def obtain_user_list():
    # Filter users based on the environment
    if os.environ['ENV'] == "TEST":
        cur.execute("SELECT id, email, first_name, last_name, interests FROM users WHERE email LIKE 'willfellhoelter%';")
    else:
        cur.execute("SELECT id, email, first_name, last_name, interests FROM users;")
    
    results = cur.fetchall()
    
    # Use dictionary comprehension to simplify user data creation
    users_list = [
        {
            'user_id': user[0],
            'user_email': user[1],
            'user_first_name': user[2],
            'user_last_name': user[3],
            'user_interests': user[4]
        }
        for user in results
    ]

    return {'list': users_list}


def obtain_posts():

    today_datetime_utc = datetime.utcnow()
    two_hours_ago = today_datetime_utc - timedelta(hours=5)

    cur.execute(f"SELECT * FROM successful_posts WHERE time between %s AND %s;",
                (two_hours_ago, today_datetime_utc))
    results = cur.fetchall()

    posts_of_the_day = {}
    posts_of_the_day['posts'] = []
    for post in results:
        post_data = {}
        post_data['successful_posts_id'] = post[0]
        post_data['subreddit'] = post[2]
        post_data['post_title'] = post[3]
        post_data['post_score'] = post[4]
        post_data['post_url'] = post[5]
        post_data['post_type'] = post[6]
        post_data['post_content'] = post[7]
        post_data['post_summary'] = post[8]
        post_data['post_title_summary'] = post[9]
        post_data['post_image_url'] = post[10]
        post_data['reddit_posts_id'] = post[11]
        post_data['post_id'] = post[12]
        post_data['post_category'] = post[13]
        post_data['post_parent_category'] = post[14]
        posts_of_the_day['posts'].append(post_data)

    return posts_of_the_day


def determine_email_templates(user_list, post_list):

    email_list = {}
    email_list['user_stories'] = []

    for user in user_list['list']:

        # Set up dict for user and stories wanted
        user_story_list = {}
        user_story_list['user_email'] = user['user_email']
        user_story_list['user_first_name'] = user['user_first_name']
        user_story_list['user_last_name'] = user['user_last_name']
        user_story_list['user_posts'] = []
        print("=================")
        print(f"Post Search | User {user['user_email']}")
        user_posts = []
        for post in post_list['posts']:
            if post['post_category'] in user['user_interests']:
                #print(
                #    f"User = {user['user_email']} | Post Category = {post['post_category']} | Post ID = {post['post_id']}")
                user_story_list['user_posts'].append(post)

        email_list['user_stories'].append(user_story_list)
    print("=================")
    return email_list


def format_article(article_data):
    return f'''
<div class="article">
  <div class="article-topic">
    <h4>{article_data['post_category'].upper()}</h4>
  </div>
    <div class="article-image">
      <a href="{article_data['post_url']}">
      <img src="{article_data['post_image_url']}" class="img-fluid">
      </a>
    </div>
    <div class="article-summary">
      <div class="article-title">
      <h2>{article_data['post_title_summary']}</h2>
      </div>
      <p>{article_data['post_summary']}</p>
    </div>
</div>
<hr>
    '''

def format_article_parent_article(parent_category):
    return f'''
<div class="parent_category">
  <div class="category">
    <h3>{parent_category}</h3>
  </div>
</div>
<hr>
    '''


def generate_newsletter(article_list, category_order_mapping, user, current_date):
    filename = f"newsletter/html/{user['user_first_name'].lower()}_{user['user_last_name'].lower()}_{current_date}.html"
    with open("newsletter/html/index.html", "r") as file:
        html_template = file.read()

    soup = BeautifulSoup(html_template, "html.parser")

    # Start by finding the leadoff div which is the starting point for insertions
    insert_point = soup.find("div", class_="leadoff")

    for order, parent_category in sorted(category_order_mapping.items(), key=lambda x: int(x[0])):
        # Insert parent category
        formatted_article = format_article_parent_article(parent_category)
        parent_soup = BeautifulSoup(formatted_article, "html.parser").div
        insert_point.insert_after(parent_soup)
        insert_point = parent_soup

        # Insert articles for the parent category
        for article in article_list['posts']:
            if article['post_category'] in user['user_interests']:
                if article['post_parent_category'] == parent_category:
                    formatted_article = format_article(article)
                    article_soup = BeautifulSoup(formatted_article, "html.parser").div
                    insert_point.insert_after(article_soup)
                    insert_point = article_soup


    with open(filename, "w") as output_file:
        output_file.write(str(soup))

    return filename

def determine_category_order():
    query = "SELECT parent_category, category_order FROM public.parent_category_hierarchy;"
    cur.execute(query)

    # Fetch rows
    rows = cur.fetchall()
    category_order_mapping = {order: category for category, order in rows}
    
    return category_order_mapping

def create_and_send_email(user_newsletter, user, current_date):
    duplicate_send = send_duplicate_check(user)
    if duplicate_send:
        return False
    msg = MIMEMultipart()
    msg['From'] = 'TheBalancedBrief@balancedbrief.com'
    msg['Subject'] = f"The Balanced Brief - {current_date}"
    msg['To'] = user['user_email']

# Read the HTML and CSS files
    with open(user_newsletter, 'r') as f:
        html_content = f.read()

    with open('newsletter/html/email-template.css', 'r') as f:
        css_content = f.read()

    # Combine the HTML and CSS
    html_with_css = f"<style>{css_content}</style>" + html_content


    # Inline the CSS
    base_path = os.path.abspath('html/')
    cssutils.log.setLevel(logging.CRITICAL)
    inlined_html = transform(html_with_css, base_url=f'file://{base_path}/')

    # Attach the processed HTML with inlined CSS to the email
    msg.attach(MIMEText(inlined_html, 'html'))
    response = None
    # Send the email
    try:
        print(f"Attempting to send email to {user['user_email']}")
        response = client.send_raw_email(
            Source=msg['From'],
            Destinations=[user['user_email']],
            RawMessage={
                'Data': msg.as_string()
            }
        )
        current_date_time = datetime.utcnow().isoformat()
        log_successful_email = sucessful_email(user, current_date_time)
        return log_successful_email

    except Exception as e:
        current_date_time = datetime.utcnow().isoformat()

        # Conditionally get the MessageId if response exists
        message_id = response['MessageId'] if response else None

        log_unsuccessful_email = unsucessful_email(user, current_date_time, str(e))
        return log_unsuccessful_email

def sucessful_email(user, current_date_time):
    print(f"{user['user_email']} - Email Successfully sent")
    data_tuple = (
        user['user_id'],
        True,
        current_date_time
    )

    # Define the INSERT statement
    insert_query = """
        INSERT INTO successful_email_sends (
            user_id,
            success,
            timestamp
        )
        VALUES (
            %s, %s, %s
        )
    """

    try:
        cur.execute(insert_query, data_tuple)
        conn.commit()
        return True

    except Exception as e:
        print(f"Failed to insert data for user {user['user_email']} on email SUCCESS. Error: {e}")
        return False

def unsucessful_email(user, current_date_time, failure_reason):
    print(f"{user['user_email']} - Email NOT sent")
    data_tuple = (
        user['user_id'],
        False,
        failure_reason,
        current_date_time
    )

    # Define the INSERT statement
    insert_query = """
        INSERT INTO unsuccessful_email_sends (
            user_id,
            success,
            failure_reason,
            timestamp
        )
        VALUES (
            %s, %s, %s, %s
        )
    """

    try:
        cur.execute(insert_query, data_tuple)
        conn.commit()
        return True

    except Exception as e:
        print(f"Failed to insert data for user {user['user_email']} on email FAILURE. Error: {e}")
        return False

def send_duplicate_check(user):
    if 'willfellhoelter' in user['user_email']:
        print("It's Will, moving through email creation")
        return False

    print(f"Running duplicate check for user {user['user_email']}")
    user_id = user['user_id']

    query = '''
        SELECT EXISTS (
            SELECT 1
            FROM successful_email_sends
            WHERE user_id = %s
            AND success = TRUE
            AND timestamp > (CURRENT_TIMESTAMP - INTERVAL '16 hours')
        );
    '''
    cur.execute(query, (user_id,))
    has_been_sent = cur.fetchone()[0]
    if not has_been_sent:
        print(f"Email has not been sent to user {user['user_email']}, going through with email template creation")
        return False
    else:
        print(f"Email has already been sent to user {user['user_email']}, moving to next user")
        return True

    return True