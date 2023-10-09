from .data import users_data

def up(cur):
    for user in users_data.USERS:
        email = user['email']
        first_name = user['first_name']
        last_name = user['last_name']
        interests = user['interests']
        age = user['age']

        print(f"Adding user {email}")

        cur.execute("""
            INSERT INTO users (email, first_name, last_name, interests, age)
            SELECT %s, %s, %s, %s, %s
            WHERE NOT EXISTS (
                SELECT 1 FROM users WHERE email = %s
            )
        """, (email, first_name, last_name, interests, age, email))

