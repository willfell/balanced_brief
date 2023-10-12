import os
if os.environ['ENV'] == "PROD":
    USERS = [
    {
        "email": "willfellhoelter@gmail.com",
        "first_name": "Will",
        "last_name": "Fellhoelter",
        "interests": ['AI', 'General News', 'World News', 'Uplifting News', 'Oddly Interesting News', 'Technology', 'Gaming', 'PC Gaming', 'Programming', 'Android', 'Apple', 'Economics', 'Finance', 'Conspiracy', 'Conservative News', 'Liberal News', 'Science', 'Sports', 'NFL', 'Soccer', 'Hockey', 'NBA', 'Movies', 'Television', 'Environment'],
        "age": 27
    },
    {
        "email": "johnw.ward4@gmail.com",
        "first_name": "John",
        "last_name": "Ward",
        "interests": ['AI', 'General News', 'World News', 'Uplifting News', 'Oddly Interesting News', 'Technology', 'Gaming', 'PC Gaming', 'Programming', 'Android', 'Apple', 'Economics', 'Finance', 'Conspiracy', 'Conservative News', 'Liberal News', 'Science', 'Sports', 'NFL', 'Soccer', 'Hockey', 'NBA', 'Movies', 'Television', 'Environment'],
        "age": 34
    },
    {
        "email": "daj.jorden@gmail.com",
        "first_name": "Daniel",
        "last_name": "Jordan",
        "interests": ['AI', 'General News', 'World News', 'Uplifting News', 'Oddly Interesting News', 'Technology', 'Gaming', 'PC Gaming', 'Programming', 'Android', 'Apple', 'Economics', 'Finance', 'Conspiracy', 'Conservative News', 'Liberal News', 'Science', 'Sports', 'NFL', 'Soccer', 'Hockey', 'NBA', 'Movies', 'Television', 'Environment'],
        "age": 26
    },
    {
        "email": "fellhoelter@gmail.com",
        "first_name": "Lance",
        "last_name": "Fellhoelter",
        "interests": ['AI', 'General News', 'World News', 'Uplifting News', 'Oddly Interesting News', 'Technology', 'Gaming', 'PC Gaming', 'Programming', 'Android', 'Apple', 'Economics', 'Finance', 'Conspiracy', 'Conservative News', 'Liberal News', 'Science', 'Sports', 'NFL', 'Soccer', 'Hockey', 'NBA', 'Movies', 'Television', 'Environment'],
        "age": 61
    },
    {
        "email": "dmfellhoelter@hotmail.com",
        "first_name": "Diana",
        "last_name": "Fellhoelter",
        "interests": ['AI', 'General News', 'World News', 'Uplifting News', 'Oddly Interesting News', 'Technology', 'Gaming', 'PC Gaming', 'Programming', 'Android', 'Apple', 'Economics', 'Finance', 'Conspiracy', 'Conservative News', 'Liberal News', 'Science', 'Sports', 'NFL', 'Soccer', 'Hockey', 'NBA', 'Movies', 'Television', 'Environment'],
        "age": 61
    },
    {
        "email": "fellhoelter13@gmail.com",
        "first_name": "Addie",
        "last_name": "Fellhoelter",
        "interests": ['AI', 'General News', 'World News', 'Uplifting News', 'Oddly Interesting News', 'Technology', 'Gaming', 'PC Gaming', 'Programming', 'Android', 'Apple', 'Economics', 'Finance', 'Conspiracy', 'Conservative News', 'Liberal News', 'Science', 'Sports', 'NFL', 'Soccer', 'Hockey', 'NBA', 'Movies', 'Television', 'Environment'],
        "age": 32
    },
    {
        "email": "breitela@gmail.com",
        "first_name": "Lydia",
        "last_name": "Breitenstein",
        "interests": ['AI', 'General News', 'World News', 'Uplifting News', 'Oddly Interesting News', 'Technology', 'Gaming', 'PC Gaming', 'Programming', 'Android', 'Apple', 'Economics', 'Finance', 'Conspiracy', 'Conservative News', 'Liberal News', 'Science', 'Sports', 'NFL', 'Soccer', 'Hockey', 'NBA', 'Movies', 'Television', 'Environment'],
        "age": 26
    },
    {
        "email": "andria.wilkes@yahoo.com",
        "first_name": "Andria",
        "last_name": "Wilkes",
        "interests": ['AI', 'General News', 'World News', 'Uplifting News', 'Oddly Interesting News', 'Technology', 'Gaming', 'PC Gaming', 'Programming', 'Android', 'Apple', 'Economics', 'Finance', 'Conspiracy', 'Conservative News', 'Liberal News', 'Science', 'Sports', 'NFL', 'Soccer', 'Hockey', 'NBA', 'Movies', 'Television', 'Environment'],
        "age": 26
    },
    {
        "email": "coolcarmie77@yahoo.com",
        "first_name": "Cool",
        "last_name": "Carmie",
        "interests": ['AI', 'General News', 'World News', 'Uplifting News', 'Oddly Interesting News', 'Technology', 'Gaming', 'PC Gaming', 'Programming', 'Android', 'Apple', 'Economics', 'Finance', 'Conspiracy', 'Conservative News', 'Liberal News', 'Science', 'Sports', 'NFL', 'Soccer', 'Hockey', 'NBA', 'Movies', 'Television', 'Environment'],
        "age": 26
    },
    {
        "email": "Hollyhox849@yahoo.com",
        "first_name": "Holly",
        "last_name": "Hox",
        "interests": ['AI', 'General News', 'World News', 'Uplifting News', 'Oddly Interesting News', 'Technology', 'Gaming', 'PC Gaming', 'Programming', 'Android', 'Apple', 'Economics', 'Finance', 'Conspiracy', 'Conservative News', 'Liberal News', 'Science', 'Sports', 'NFL', 'Soccer', 'Hockey', 'NBA', 'Movies', 'Television', 'Environment'],
        "age": 26
    }
    ]
else:
    USERS = [
        {
            "email": "willfellhoelter@gmail.com",
            "first_name": "Will",
            "last_name": "Fell",
            "interests": ['AI', 'General News', 'World News', 'Uplifting News', 'Oddly Interesting News', 'Technology', 'Gaming', 'PC Gaming', 'Programming', 'Android', 'Apple', 'Economics', 'Finance', 'Conspiracy', 'Conservative News', 'Liberal News', 'Science', 'Sports', 'NFL', 'Soccer', 'Hockey', 'NBA', 'Movies', 'Television', 'Environment'],
            "age": 27
        },
        {
            "email": "willfellhoelter+test@gmail.com",
            "first_name": "Will",
            "last_name": "Fell",
            "interests": ['AI', 'World News', 'Uplifting News', 'Economics', 'Conservative News', 'NFL', 'Movies'],
            "age": 27
        },
        {
            "email": "willfellhoelter+test@foobarfakewebsite.com",
            "first_name": "Will",
            "last_name": "Fell",
            "interests": ['AI', 'World News', 'Uplifting News', 'Economics', 'Conservative News', 'NFL', 'Movies'],
            "age": 27
        }
    ]
