import os
if os.environ['ENV'] == "PROD":
    SUBREDDITS_TO_RETRIEVE = [
        {
            "subreddit_name": "Conservative",
            "subreddit_category": "Conservative News",
            "subreddit_parent_category": "Catered News"
        },
        {
            "subreddit_name": "Libertarian",
            "subreddit_category": "Liberal News",
            "subreddit_parent_category": "Catered News"
        },
        {
            "subreddit_name": "environment",
            "subreddit_category": "Environment",
            "subreddit_parent_category": "Catered News"
        },
        {
            "subreddit_name": "movies",
            "subreddit_category": "Movies",
            "subreddit_parent_category": "Entertainment"
        },
        {
            "subreddit_name": "television",
            "subreddit_category": "Television",
            "subreddit_parent_category": "Entertainment"
        },
        {
            "subreddit_name": "Economics",
            "subreddit_category": "Economics",
            "subreddit_parent_category": "Finance"
        },
        {
            "subreddit_name": "Finance",
            "subreddit_category": "Finance",
            "subreddit_parent_category": "Finance"
        },
        {
            "subreddit_name": "worldnews",
            "subreddit_category": "World News",
            "subreddit_parent_category": "News"
        },
        {
            "subreddit_name": "news",
            "subreddit_category": "General News",
            "subreddit_parent_category": "News"
        },
        {
            "subreddit_name": "UpliftingNews",
            "subreddit_category": "Uplifting News",
            "subreddit_parent_category": "Offbeat News"
        },
        {
            "subreddit_name": "nottheonion",
            "subreddit_category": "Oddly Interesting News",
            "subreddit_parent_category": "Offbeat News"
        },
        {
            "subreddit_name": "conspiracy",
            "subreddit_category": "Conspiracy",
            "subreddit_parent_category": "Offbeat News"
        },
        {
            "subreddit_name": "sports",
            "subreddit_category": "Sports",
            "subreddit_parent_category": "Sports"
        },
        {
            "subreddit_name": "nfl",
            "subreddit_category": "NFL",
            "subreddit_parent_category": "Sports"
        },
        {
            "subreddit_name": "soccer",
            "subreddit_category": "Soccer",
            "subreddit_parent_category": "Sports"
        },
        {
            "subreddit_name": "hockey",
            "subreddit_category": "Hockey",
            "subreddit_parent_category": "Sports"
        },
        {
            "subreddit_name": "nba",
            "subreddit_category": "NBA",
            "subreddit_parent_category": "Sports"
        },
        {
            "subreddit_name": "technology",
            "subreddit_category": "Technology",
            "subreddit_parent_category": "Tech News"
        },
        {
            "subreddit_name": "gaming",
            "subreddit_category": "Gaming",
            "subreddit_parent_category": "Tech News"
        },
        {
            "subreddit_name": "pcgaming",
            "subreddit_category": "PC Gaming",
            "subreddit_parent_category": "Tech News"
        },
        {
            "subreddit_name": "programming",
            "subreddit_category": "Programming",
            "subreddit_parent_category": "Tech News"
        },
        {
            "subreddit_name": "Android",
            "subreddit_category": "Android",
            "subreddit_parent_category": "Tech News"
        },
        {
            "subreddit_name": "apple",
            "subreddit_category": "Apple",
            "subreddit_parent_category": "Tech News"
        },
        {
            "subreddit_name": "science",
            "subreddit_category": "Science",
            "subreddit_parent_category": "Tech News"
        },
        {
            "subreddit_name": "artificial",
            "subreddit_category": "AI",
            "subreddit_parent_category": "Tech News"
        }
    ]
else:
    SUBREDDITS_TO_RETRIEVE = [
        {
            "subreddit_name": "Conservative",
            "subreddit_category": "Conservative News",
            "subreddit_parent_category": "Catered News"
        },
        {
            "subreddit_name": "Libertarian",
            "subreddit_category": "Liberal News",
            "subreddit_parent_category": "Catered News"
        },
        {
            "subreddit_name": "environment",
            "subreddit_category": "Environment",
            "subreddit_parent_category": "Catered News"
        },
        {
            "subreddit_name": "RenewableEnergy",
            "subreddit_category": "Renewable Energy",
            "subreddit_parent_category": "Catered News"
        },
        {
            "subreddit_name": "movies",
            "subreddit_category": "Movies",
            "subreddit_parent_category": "Entertainment"
        },
        {
            "subreddit_name": "television",
            "subreddit_category": "Television",
            "subreddit_parent_category": "Entertainment"
        },
        {
            "subreddit_name": "books",
            "subreddit_category": "Books",
            "subreddit_parent_category": "Entertainment"
        },
        {
            "subreddit_name": "Economics",
            "subreddit_category": "Economics",
            "subreddit_parent_category": "Finance"
        },
        {
            "subreddit_name": "Finance",
            "subreddit_category": "Finance",
            "subreddit_parent_category": "Finance"
        },
        {
            "subreddit_name": "news",
            "subreddit_category": "General News",
            "subreddit_parent_category": "News"
        },
        {
            "subreddit_name": "worldnews",
            "subreddit_category": "World News",
            "subreddit_parent_category": "News"
        },
        {
            "subreddit_name": "offbeat",
            "subreddit_category": "Off Beat News",
            "subreddit_parent_category": "Offbeat News"
        },
        {
            "subreddit_name": "UpliftingNews",
            "subreddit_category": "Uplifting News",
            "subreddit_parent_category": "Offbeat News"
        },
        {
            "subreddit_name": "nottheonion",
            "subreddit_category": "Oddly Interesting News",
            "subreddit_parent_category": "Offbeat News"
        },
        {
            "subreddit_name": "conspiracy",
            "subreddit_category": "Conspiracy",
            "subreddit_parent_category": "Offbeat News"
        },
        {
            "subreddit_name": "sports",
            "subreddit_category": "Sports",
            "subreddit_parent_category": "Sports"
        },
        {
            "subreddit_name": "nfl",
            "subreddit_category": "NFL",
            "subreddit_parent_category": "Sports"
        },
        {
            "subreddit_name": "soccer",
            "subreddit_category": "Soccer",
            "subreddit_parent_category": "Sports"
        },
        {
            "subreddit_name": "hockey",
            "subreddit_category": "Hockey",
            "subreddit_parent_category": "Sports"
        },
        {
            "subreddit_name": "nba",
            "subreddit_category": "NBA",
            "subreddit_parent_category": "Sports"
        },
        {
            "subreddit_name": "technology",
            "subreddit_category": "Technology",
            "subreddit_parent_category": "Tech News"
        },
        {
            "subreddit_name": "Futurology",
            "subreddit_category": "Futurology",
            "subreddit_parent_category": "Tech News"
        },
        {
            "subreddit_name": "Games",
            "subreddit_category": "Games",
            "subreddit_parent_category": "Tech News"
        },
        {
            "subreddit_name": "gaming",
            "subreddit_category": "Gaming",
            "subreddit_parent_category": "Tech News"
        },
        {
            "subreddit_name": "pcgaming",
            "subreddit_category": "PC Gaming",
            "subreddit_parent_category": "Tech News"
        },
        {
            "subreddit_name": "programming",
            "subreddit_category": "Programming",
            "subreddit_parent_category": "Tech News"
        },
        {
            "subreddit_name": "Android",
            "subreddit_category": "Android",
            "subreddit_parent_category": "Tech News"
        },
        {
            "subreddit_name": "apple",
            "subreddit_category": "Apple",
            "subreddit_parent_category": "Tech News"
        },
        {
            "subreddit_name": "science",
            "subreddit_category": "Science",
            "subreddit_parent_category": "Tech News"
        },
        {
            "subreddit_name": "artificial",
            "subreddit_category": "AI",
            "subreddit_parent_category": "Tech News"
        }
    ]


