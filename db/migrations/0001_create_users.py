def up(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                (id SERIAL PRIMARY KEY,
                email TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                interests TEXT[] NOT NULL,
                date_of_birth DATE NOT NULL,
                verified BOOLEAN DEFAULT FALSE,
                verified_at TIMESTAMP NULL);''')
