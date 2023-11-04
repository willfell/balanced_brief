def up(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS users
                (id SERIAL PRIMARY KEY,
                email TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                interests TEXT[] NOT NULL,
                age INTEGER NOT NULL,
                verified BOOLEAN DEFAULT FALSE);''')
    
