import praw
import os
import requests
from bs4 import BeautifulSoup
from newspaper import Article
import json
from functions_ import *
from datetime import datetime


# Replace the following variables with your Reddit API app credentials
RDT_CLIENT_ID = os.environ["REDDITCLIENTID"]
RDT_CLIENT_SECRET = os.environ["REDDITCLIENTSECRET"]
user_agent = os.environ["REDDITAGENT"]

# Testing variables
testing = "all"
use_gpt = True


def gather_articles():
    to_brief = {}
    to_brief["reddit_posts"] = []

    # Initialize the Reddit instance with your credentials
    reddit = praw.Reddit(
        client_id=RDT_CLIENT_ID, client_secret=RDT_CLIENT_SECRET, user_agent=user_agent
    )

    def get_top_post_of_day(subreddit_name):
        print("============================")
        print(f"Gathering post for /r/{subreddit_name}")
        subreddit = reddit.subreddit(subreddit_name)
        top_post = subreddit.top(time_filter="day", limit=60)

        for post in top_post:
            # Filter out bad posts
            if "jpg" in post.url:
                print(
                    f"Post URL appears to be a url with an image in it {post.url}, skipping"
                )
                continue
            elif "redd" in post.url:
                print(f"Post URL has reddit in it with url {post.url}, skipping")
                continue
            else:
                post_type = "article"

            is_duplicate = is_it_duplicate(post.id)
            if is_duplicate:
                print(f"Duplicate post for {subreddit}, skipping")
                break

            # Check to see if you're able to scrape from what you have
            scrapable = is_it_scrapable(post.url, subreddit)
            if not scrapable:
                continue

            category = get_category(subreddit)
            parent_category = get_parent_category(subreddit)

            reddit_post_id = submit_reddit_post_to_db(
                post, subreddit_name, post_type, category, parent_category
            )

            print(f"Successfuly obtained story of the day for {subreddit}")
            print("===================================")
            return True

    subreddits = determine_subreddits()

    for subreddit in subreddits:
        get_top_post_of_day(subreddit)

    return to_brief


def scrape(post):
    print("=================")
    print(f"Attempting to post for subreddit r/{post['subreddit']}")
    is_duplicate = is_scrape_duplicate(post["post_id"])
    if is_duplicate:
        print(f"Duplicate post for {post['subreddit']}, skipping")
        print("=================")
        return False

    scraped_content = scrape_post_content(post)

    # Create summary to articles
    if use_gpt:
        scraped_content["post_summary"] = proomptThatShit(
            scraped_content["post_content"]
        )
        scraped_content["post_title_summary"] = proompt_summary_to_title(
            scraped_content["article_title"]
        )
    else:
        scraped_content["post_summary"] = "summarized article here"
        scraped_content["post_title_summary"] = scraped_content["article_title"]

    # Submit the summary and all other data to the db
    submit_post_to_db = submit_successful_post_to_db(scraped_content)
    return submit_post_to_db


if testing == "all":
    posts = gather_articles()
    posts_to_scrape = gather_articles_to_scrape()
    for post in posts_to_scrape["reddit_posts"]:
        summarized_articles = scrape(post)
elif testing == "gather":
    posts = gather_articles
else:
    posts_to_scrape = gather_articles_to_scrape()
    for post in posts_to_scrape["reddit_posts"]:
        summarized_articles = scrape(post)
