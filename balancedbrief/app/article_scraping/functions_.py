import os
from openai import OpenAI
import openai
import time
import psycopg2
import json
from newspaper import Article
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import boto3

# GPT Config
temperature = 0.5
# gpt_model = 'gpt-4-1106-preview'
gpt_model = "gpt-3.5-turbo-16k"
client = OpenAI(api_key=os.environ["OPENAI_KEY"])

# DB Config
db_pass = os.environ["POSTGRES_DB_PASS"]
db_host = os.environ["POSTGRES_DB_HOST"]
conn_params = {
    "host": db_host,
    "port": "5432",
    "database": "postgres",
    "user": "db_user",
    "password": db_pass,
}

# Create a new connection and cursor object
conn = psycopg2.connect(**conn_params)
cur = conn.cursor()


def proomptThatShit(scraped_article, retries=5, delay=5):
    print(f"Length of article before trimming = {len(scraped_article)}")
    max_length = 10000
    if len(scraped_article) >= max_length:
        print("Trimming content")
        scraped_article = scraped_article[:max_length].rsplit(" ", 1)[0]
        print(f"New length for the content is {len(scraped_article)}")

    system_prompt = f"Assistant, please summarize the following article professionally in 50 words or less so that a 30 year old can understand it"
    prompt_length = len(system_prompt + scraped_article)
    max_output_tokens = int(1.5 * 300)  # 200 words * 1.5 tokens/word = 300 tokens
    buffer = int(0.1 * max_output_tokens)  # 10% buffer = 30 tokens
    max_tokens = prompt_length + max_output_tokens + buffer
    print(f"Tokens desired = {max_tokens}")

    model_engine = gpt_model

    messages = [
        {"role": "system", "content": f"{system_prompt}"},
        {"role": "user", "content": scraped_article},
    ]

    base_delay = 1  # Start with a 1 second delay
    backoff_multiplier = 2  # Use a backoff multiplier of 2

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=model_engine,
                messages=messages,
                temperature=temperature,  # ensure 'temperature' is defined in your code
                max_tokens=max_tokens,
                n=1,
                stop=None,
                presence_penalty=0.0,
                frequency_penalty=0.0,
            )
            if response.choices:
                content = response.choices[0].message.content
                return content
        except openai.APIError as e:
            # If it's the last retry, raise the exception
            if attempt == retries - 1:
                raise e
            print(
                f"Error on attempt {attempt + 1}: {e}. Retrying in {delay} seconds..."
            )
            # Apply exponential backoff with a cap of 32 seconds
            delay = min(base_delay * (backoff_multiplier**attempt), 32)
            print(
                f"Error on attempt {attempt + 1}: {e}. Retrying in {delay} seconds..."
            )
            time.sleep(delay)  # wait for some time before retrying

    return None


def proompt_summary_to_title(article_summary, retries=5, delay=5):
    max_length = 2500
    model_engine = gpt_model

    system_prompt = f"Assistant, make a short and sweet article headline out of the following text without the use of quotes around it"
    prompt_length = len(system_prompt + article_summary)
    max_output_tokens = int(1.5 * 15)  # 15 words * 1.5 tokens/word = 22.5 tokens
    buffer = int(0.1 * max_output_tokens)  # 10% buffer
    max_tokens = prompt_length + max_output_tokens + buffer
    print(f"Tokens desired for title = {max_tokens}")

    messages = [
        {"role": "system", "content": f"{system_prompt}"},
        {"role": "user", "content": article_summary},
    ]

    base_delay = 1  # Start with a 1 second delay
    backoff_multiplier = 2  # Use a backoff multiplier of 2

    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model=model_engine,
                messages=messages,
                temperature=temperature,  # ensure 'temperature' is defined in your code
                max_tokens=max_tokens,
                n=1,
                stop=None,
                presence_penalty=0.0,
                frequency_penalty=0.0,
            )
            if response.choices:
                content = response.choices[0].message.content
                return content
        except openai.APIError as e:
            # If it's the last retry, raise the exception
            if attempt == retries - 1:
                raise e
            print(
                f"Error on attempt {attempt + 1}: {e}. Retrying in {delay} seconds..."
            )
            # Apply exponential backoff with a cap of 32 seconds
            delay = min(base_delay * (backoff_multiplier**attempt), 32)
            print(
                f"Error on attempt {attempt + 1}: {e}. Retrying in {delay} seconds..."
            )
            time.sleep(delay)  # wait for some time before retrying
    return None


def get_category(subreddit):
    cur.execute(
        f"SELECT category from subreddits where subreddit_name = '{subreddit}';"
    )
    results = cur.fetchall()
    category = results[0][0]
    return category


def get_parent_category(subreddit):
    cur.execute(
        f"SELECT parent_category from subreddits where subreddit_name = '{subreddit}';"
    )
    results = cur.fetchall()
    parent_category = results[0][0]
    return parent_category


def determine_subreddits():
    cur.execute("SELECT subreddit_name FROM subreddits;")
    results = cur.fetchall()
    subreddit_names = [result[0] for result in results]
    return subreddit_names


def submit_unsuccessful_post_to_db(post):
    data_tuple = (
        datetime.utcnow(),
        post["reddit_posts_id"],
        post["post_id"],
        post["subreddit"],
        post["post_title"],
        post["post_score"],
        post["post_url"],
        post["post_type"],
        post["post_category"],
    )

    # Define the INSERT statement
    insert_query = """
        INSERT INTO unsuccessful_posts (
            time,
            reddit_posts_id,
            post_id,
            subreddit,
            post_title,
            post_score,
            post_url,
            post_type,
            post_category
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    # Execute the INSERT statement
    cur.execute(insert_query, data_tuple)
    conn.commit()
    print(f"Unsuccessful post for subreddit r/{post['subreddit']}")
    print("=================")
    return True


def submit_successful_post_to_db(post):
    data_tuple = (
        datetime.utcnow(),
        post["reddit_posts_id"],
        post["post_id"],
        post["subreddit"],
        post["post_title"],
        post["post_score"],
        post["post_url"],
        post["post_type"],
        post["post_content"],
        post["post_summary"],
        post["post_title_summary"],
        post["post_image_url"],
        post["post_category"],
        post["post_parent_category"],
        post["article_title"],
        post["article_authors"],
        post["article_publish_date"],
        post["article_source_url"],
    )

    print(post["reddit_posts_id"])
    print(post["post_id"])
    print(post["subreddit"])
    print(post["post_title"])
    print(post["post_score"])
    print(post["post_url"])
    print(post["post_type"])
    print(post["post_content"])
    print(post["post_summary"])
    print(post["post_title_summary"])
    print(post["post_image_url"])
    print(post["post_category"])
    print(post["post_parent_category"])
    print(post["article_title"])
    print(post["article_authors"])
    print(post["article_publish_date"])
    print(post["article_source_url"])

    # Define the INSERT statement
    insert_query = """
        INSERT INTO successful_posts (
            time,
            reddit_posts_id,
            post_id,
            subreddit,
            post_title,
            post_score,
            post_url,
            post_type,
            post_content,
            post_summary,
            post_title_summary,
            post_image_url,
            post_category,
            post_parent_category,
            article_title,
            article_authors,
            article_publish_date,
            article_source_url
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
    """

    # Execute the INSERT statement
    cur.execute(insert_query, data_tuple)
    conn.commit()
    print(f"Successful post for subreddit r/{post['subreddit']}")
    print("=================")
    return True


def submit_reddit_post_to_db(post, subreddit, post_type, category, parent_category):
    post_title = post.title
    post_title = post_title.encode("windows-1252", errors="ignore").decode(
        "utf-8", errors="ignore"
    )

    json_data = {
        "time": datetime.utcnow(),
        "subreddit": subreddit,
        "post_title": post_title,
        "post_score": post.score,
        "post_url": post.url,
        "post_type": post_type,
        "post_category": category,
        "post_parent_category": parent_category,
        "post_id": post.id,
    }

    data_tuple = (
        json_data["time"],
        json_data["subreddit"],
        json_data["post_title"],
        json_data["post_score"],
        json_data["post_url"],
        json_data["post_type"],
        json_data["post_category"],
        json_data["post_parent_category"],
        json_data["post_id"],
    )

    # Define the INSERT statement
    insert_query = """
        INSERT INTO reddit_posts (
            time,
            subreddit,
            post_title,
            post_score,
            post_url,
            post_type,
            post_category,
            post_parent_category,
            post_id
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        RETURNING id
    """

    # Execute the INSERT statement
    cur.execute(insert_query, data_tuple)
    conn.commit()

    return True


def is_it_scrapable(url, subreddit):
    min_article_length = 400
    article = Article(url)
    try:
        article.download()
        article.parse()
        html = article.html
        soup = BeautifulSoup(html, "html.parser")

        if article.clean_top_node is not None:
            main_content_element = soup.find(
                article.clean_top_node.tag, class_=article.clean_top_node.get("class")
            )

            if main_content_element:
                post_content = main_content_element.get_text(strip=True)
                if len(post_content) < min_article_length:
                    return False

                if post_content == "":
                    return False

                print(f"Article {url} | subreddit {subreddit} | Success scraping")
                return True
            else:
                return False
        else:
            return False
    except:
        return False


def scrape_post_content(post):
    article = Article(post["post_url"])

    try:
        article.download()
        article.parse()
        html = article.html
        soup = BeautifulSoup(html, "html.parser")

        main_content_element = soup.find(
            article.clean_top_node.tag, class_=article.clean_top_node.get("class")
        )

        post["article_title"] = article.title
        post["article_authors"] = article.authors
        post["article_publish_date"] = str(article.publish_date)
        post["article_source_url"] = article.source_url
        post["post_image_url"] = article.top_image
        post["post_content"] = main_content_element.get_text(strip=True)
    except:
        print(
            f"Article Scraping failed for URL {post['post_url']}\nsubmitting to unsuccessful_posts"
        )
        submit_unsuccessful_post_to_db(post)

    return post


def is_it_duplicate(post_id):
    cur.execute(f"SELECT id from reddit_posts where post_id = '{post_id}';")
    results = cur.fetchall()

    if results == []:
        return False
    else:
        return True


def is_scrape_duplicate(post_id):
    cur.execute(f"SELECT id from successful_posts where post_id = '{post_id}';")
    results = cur.fetchall()

    if results == []:
        return False
    else:
        return True


def gather_articles_to_scrape():
    today_datetime_utc = datetime.utcnow()
    yesterday_datetime_utc = today_datetime_utc - timedelta(days=1)

    cur.execute(
        f"SELECT * FROM reddit_posts WHERE time between %s AND %s;",
        (yesterday_datetime_utc, today_datetime_utc),
    )
    results = cur.fetchall()

    articles_to_scrape = {}
    articles_to_scrape["reddit_posts"] = []
    for article in results:
        article_data = {}
        article_data["reddit_posts_id"] = article[0]
        article_data["post_id"] = article[1]
        article_data["subreddit"] = article[3]
        article_data["post_title"] = article[4]
        article_data["post_score"] = article[5]
        article_data["post_url"] = article[6]
        article_data["post_type"] = article[7]
        article_data["post_category"] = article[8]
        article_data["post_parent_category"] = article[9]
        articles_to_scrape["reddit_posts"].append(article_data)

    return articles_to_scrape