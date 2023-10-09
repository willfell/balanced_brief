def up(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS reddit_posts
                (id SERIAL PRIMARY KEY,
                post_id TEXT NOT NULL UNIQUE,
                    time TIMESTAMP NOT NULL,
                    subreddit TEXT NOT NULL,
                    post_title TEXT NOT NULL,
                    post_score INTEGER NOT NULL,
                    post_url TEXT NOT NULL,
                    post_type TEXT NOT NULL,
                    post_category TEXT NOT NULL,
                    post_parent_category TEXT NOT NULL);''')

    cur.execute('''CREATE TABLE IF NOT EXISTS unsuccessful_posts
                (id SERIAL PRIMARY KEY,
                    time TIMESTAMP NOT NULL,
                    subreddit TEXT NOT NULL,
                    post_title TEXT NOT NULL,
                    post_score INTEGER NOT NULL,
                    post_url TEXT NOT NULL,
                    post_type TEXT NOT NULL,
                    post_scrape_fail_reason TEXT,
                    reddit_posts_id INTEGER NOT NULL REFERENCES reddit_posts(id),
                    post_id TEXT NOT NULL UNIQUE REFERENCES reddit_posts(post_id),
                    post_category TEXT NOT NULL,
                    post_parent_category TEXT NOT NULL,
                    article_title TEXT,
                    article_authors TEXT[],
                    article_publish_date TEXT,
                    article_source_url TEXT);''')

    cur.execute('''CREATE TABLE IF NOT EXISTS successful_posts
                (id SERIAL PRIMARY KEY,
                    time TIMESTAMP NOT NULL,
                    subreddit TEXT NOT NULL,
                    post_title TEXT NOT NULL,
                    post_score INTEGER NOT NULL,
                    post_url TEXT NOT NULL,
                    post_type TEXT NOT NULL,
                    post_content TEXT,
                    post_summary TEXT,
                    post_title_summary TEXT,
                    post_image_url TEXT,
                    reddit_posts_id INTEGER NOT NULL REFERENCES reddit_posts(id),
                    post_id TEXT NOT NULL UNIQUE REFERENCES reddit_posts(post_id),
                    post_category TEXT NOT NULL,
                    post_parent_category TEXT NOT NULL,
                    article_title TEXT,
                    article_authors TEXT[],
                    article_publish_date TEXT,
                    article_source_url TEXT);''')

