from .data import subreddits

def up(cur):
    """Creates the subreddits table if it doesn't exist."""
    cur.execute('''
        CREATE TABLE IF NOT EXISTS subreddits
        (id SERIAL PRIMARY KEY,
        subreddit_name TEXT UNIQUE NOT NULL,
        category TEXT NOT NULL,
        parent_category TEXT NOT NULL);
    ''')
    print("Successfully created subreddits")
