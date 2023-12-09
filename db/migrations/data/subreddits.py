import os

SUBREDDITS_TO_RETRIEVE = [
    {
        "subreddit_name": "Conservative",
        "subreddit_category": "Conservative News",
        "subreddit_parent_category": "Catered News",
    },
    {
        "subreddit_name": "Libertarian",
        "subreddit_category": "Liberal News",
        "subreddit_parent_category": "Catered News",
    },
    {
        "subreddit_name": "environment",
        "subreddit_category": "Environment",
        "subreddit_parent_category": "Catered News",
    },
    {
        "subreddit_name": "RenewableEnergy",
        "subreddit_category": "Renewable Energy",
        "subreddit_parent_category": "Catered News",
    },
    {
        "subreddit_name": "movies",
        "subreddit_category": "Movies",
        "subreddit_parent_category": "Entertainment",
    },
    {
        "subreddit_name": "television",
        "subreddit_category": "Television",
        "subreddit_parent_category": "Entertainment",
    },
    {
        "subreddit_name": "books",
        "subreddit_category": "Books",
        "subreddit_parent_category": "Entertainment",
    },
    {
        "subreddit_name": "Economics",
        "subreddit_category": "Economics",
        "subreddit_parent_category": "Finance",
    },
    {
        "subreddit_name": "Finance",
        "subreddit_category": "Finance",
        "subreddit_parent_category": "Finance",
    },
    {
        "subreddit_name": "news",
        "subreddit_category": "General News",
        "subreddit_parent_category": "News",
    },
    {
        "subreddit_name": "worldnews",
        "subreddit_category": "World News",
        "subreddit_parent_category": "News",
    },
    {
        "subreddit_name": "offbeat",
        "subreddit_category": "Off Beat News",
        "subreddit_parent_category": "Offbeat News",
    },
    {
        "subreddit_name": "UpliftingNews",
        "subreddit_category": "Uplifting News",
        "subreddit_parent_category": "Offbeat News",
    },
    {
        "subreddit_name": "nottheonion",
        "subreddit_category": "Oddly Interesting News",
        "subreddit_parent_category": "Offbeat News",
    },
    {
        "subreddit_name": "conspiracy",
        "subreddit_category": "Conspiracy",
        "subreddit_parent_category": "Offbeat News",
    },
    {
        "subreddit_name": "sports",
        "subreddit_category": "Sports",
        "subreddit_parent_category": "Sports",
    },
    {
        "subreddit_name": "nfl",
        "subreddit_category": "NFL",
        "subreddit_parent_category": "Sports",
    },
    {
        "subreddit_name": "soccer",
        "subreddit_category": "Soccer",
        "subreddit_parent_category": "Sports",
    },
    {
        "subreddit_name": "hockey",
        "subreddit_category": "Hockey",
        "subreddit_parent_category": "Sports",
    },
    {
        "subreddit_name": "nba",
        "subreddit_category": "NBA",
        "subreddit_parent_category": "Sports",
    },
    {
        "subreddit_name": "technology",
        "subreddit_category": "Technology",
        "subreddit_parent_category": "Tech News",
    },
    {
        "subreddit_name": "Futurology",
        "subreddit_category": "Futurology",
        "subreddit_parent_category": "Tech News",
    },
    {
        "subreddit_name": "Games",
        "subreddit_category": "Games",
        "subreddit_parent_category": "Tech News",
    },
    {
        "subreddit_name": "gaming",
        "subreddit_category": "Gaming",
        "subreddit_parent_category": "Tech News",
    },
    {
        "subreddit_name": "pcgaming",
        "subreddit_category": "PC Gaming",
        "subreddit_parent_category": "Tech News",
    },
    {
        "subreddit_name": "programming",
        "subreddit_category": "Programming",
        "subreddit_parent_category": "Tech News",
    },
    {
        "subreddit_name": "Android",
        "subreddit_category": "Android",
        "subreddit_parent_category": "Tech News",
    },
    {
        "subreddit_name": "apple",
        "subreddit_category": "Apple",
        "subreddit_parent_category": "Tech News",
    },
    {
        "subreddit_name": "science",
        "subreddit_category": "Science",
        "subreddit_parent_category": "Tech News",
    },
    {
        "subreddit_name": "artificial",
        "subreddit_category": "AI",
        "subreddit_parent_category": "Tech News",
    },
    {
        "subreddit_name": "Alabama",
        "subreddit_category": "Alabama",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "alaska",
        "subreddit_category": "Alaska",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "arizona",
        "subreddit_category": "Arizona",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Arkansas",
        "subreddit_category": "Arkansas",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "California",
        "subreddit_category": "California",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Colorado",
        "subreddit_category": "Colorado",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Connecticut",
        "subreddit_category": "Connecticut",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Delaware",
        "subreddit_category": "Delaware",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "florida",
        "subreddit_category": "Florida",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Georgia",
        "subreddit_category": "Georgia",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Hawaii",
        "subreddit_category": "Hawaii",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Idaho",
        "subreddit_category": "Idaho",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "illinois",
        "subreddit_category": "Illinois",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Indiana",
        "subreddit_category": "Indiana",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Iowa",
        "subreddit_category": "Iowa",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "kansas",
        "subreddit_category": "Kansas",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Kentucky",
        "subreddit_category": "Kentucky",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Louisiana",
        "subreddit_category": "Louisiana",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Maine",
        "subreddit_category": "Maine",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "maryland",
        "subreddit_category": "Maryland",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "massachusetts",
        "subreddit_category": "Massachusetts",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Michigan",
        "subreddit_category": "Michigan",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "minnesota",
        "subreddit_category": "Minnesota",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "mississippi",
        "subreddit_category": "Mississippi",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "missouri",
        "subreddit_category": "Missouri",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Montana",
        "subreddit_category": "Montana",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Nebraska",
        "subreddit_category": "Nebraska",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Nevada",
        "subreddit_category": "Nevada",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "newhampshire",
        "subreddit_category": "New Hampshire",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "newjersey",
        "subreddit_category": "New Jersey",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "NewMexico",
        "subreddit_category": "New Mexico",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "newyork",
        "subreddit_category": "New York",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "NorthCarolina",
        "subreddit_category": "North Carolina",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "northdakota",
        "subreddit_category": "North Dakota",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Ohio",
        "subreddit_category": "Ohio",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "oklahoma",
        "subreddit_category": "Oklahoma",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "oregon",
        "subreddit_category": "Oregon",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Pennsylvania",
        "subreddit_category": "Pennsylvania",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "RhodeIsland",
        "subreddit_category": "Rhode Island",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "southcarolina",
        "subreddit_category": "South Carolina",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "SouthDakota",
        "subreddit_category": "South Dakota",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Tennessee",
        "subreddit_category": "Tennessee",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "texas",
        "subreddit_category": "Texas",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Utah",
        "subreddit_category": "Utah",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "vermont",
        "subreddit_category": "Vermont",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Virginia",
        "subreddit_category": "Virginia",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "Washington",
        "subreddit_category": "Washington",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "WestVirginia",
        "subreddit_category": "West Virginia",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "wisconsin",
        "subreddit_category": "Wisconsin",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "wyoming",
        "subreddit_category": "Wyoming",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "wyoming",
        "subreddit_category": "Wyoming",
        "subreddit_parent_category": "US Local News",
    },
    {
        "subreddit_name": "alberta",
        "subreddit_category": "Alberta",
        "subreddit_parent_category": "Canada Local News",
    },
    {
        "subreddit_name": "britishcolumbia",
        "subreddit_category": "British Columbia",
        "subreddit_parent_category": "Canada Local News",
    },
    {
        "subreddit_name": "Manitoba",
        "subreddit_category": "Manitoba",
        "subreddit_parent_category": "Canada Local News",
    },
    {
        "subreddit_name": "newbrunswickcanada",
        "subreddit_category": "New Brunswick",
        "subreddit_parent_category": "Canada Local News",
    },
    {
        "subreddit_name": "newfoundland",
        "subreddit_category": "Newfoundland and Labrador",
        "subreddit_parent_category": "Canada Local News",
    },
    {
        "subreddit_name": "NovaScotia",
        "subreddit_category": "Nova Scotia",
        "subreddit_parent_category": "Canada Local News",
    },
    {
        "subreddit_name": "ontario",
        "subreddit_category": "Ontario",
        "subreddit_parent_category": "Canada Local News",
    },
    {
        "subreddit_name": "PEI",
        "subreddit_category": "Prince Edward Island",
        "subreddit_parent_category": "Canada Local News",
    },
    {
        "subreddit_name": "Quebec",
        "subreddit_category": "Quebec",
        "subreddit_parent_category": "Canada Local News",
    },
    {
        "subreddit_name": "saskatchewan",
        "subreddit_category": "saskatchewan",
        "subreddit_parent_category": "Canada Local News",
    },
]
