import os
import psycopg2
import json
from newspaper import Article
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

html_dir = 'html'


# set up connection parameters
db_pass = os.environ['DB_PASS']
db_host = os.environ['DB_HOST']
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
    cur.execute("SELECT * FROM users;")
    results = cur.fetchall()
    users = {}
    users['list'] = []
    for user in results:
        user_data = {}
        user_data['user_id'] = user[0]
        user_data['user_email'] = user[1]
        user_data['user_first_name'] = user[2]
        user_data['user_last_name'] = user[3]
        user_data['user_interests'] = user[4]
        user_data['user_age'] = user[5]
        users['list'].append(user_data)

    return users


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


def generate_newsletter(articles, filename, category_order_mapping):
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
        for article in articles:
            if article['post_parent_category'] == parent_category:
                formatted_article = format_article(article)
                article_soup = BeautifulSoup(formatted_article, "html.parser").div
                insert_point.insert_after(article_soup)
                insert_point = article_soup


    with open(filename, "w") as output_file:
        output_file.write(str(soup))

def create_email_templates(email_list, category_order_mapping):

    for stories in email_list['user_stories']:
        print("=================")
        print(f"Creating email template for {stories['user_email']}")
        filename = f"newsletter/{html_dir}/{stories['user_first_name'].lower()}_{stories['user_last_name'].lower()}.html"

        # Generate the newsletter as that function iterates through the list anyways
        generate_newsletter(stories['user_posts'], filename, category_order_mapping)

def retrieve_email_list():
    query = "SELECT email FROM public.user_send_list;"
    cur.execute(query)

    # Fetch all rows from the result
    rows = cur.fetchall()

    # Convert the rows into a list of emails
    emails = [row[0] for row in rows]

    return(emails)  # This will print the list of emails


def determine_category_order():
    query = "SELECT parent_category, category_order FROM public.parent_category_hierarchy;"
    cur.execute(query)

    # Fetch rows
    rows = cur.fetchall()
    category_order_mapping = {order: category for category, order in rows}
    
    return category_order_mapping