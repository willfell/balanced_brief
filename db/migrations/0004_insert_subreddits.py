from .data import subreddits

def up(cur):
    for subreddit in subreddits.SUBREDDITS_TO_RETRIEVE:
        """Adds a subreddit entry to the subreddits table if it doesn't exist."""
        subreddit_name = subreddit['subreddit_name']
        subreddit_category = subreddit['subreddit_category']
        subreddit_parent_category = subreddit['subreddit_parent_category']

        cur.execute("""
            INSERT INTO subreddits (subreddit_name, category, parent_category)
            SELECT %s, %s, %s
            WHERE NOT EXISTS (
                SELECT 1 FROM subreddits WHERE subreddit_name = %s
            )
        """, (subreddit_name, subreddit_category, subreddit_parent_category, subreddit_name))
