def up(cur):
    # Create successful_email_sends table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS successful_email_sends (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        success BOOLEAN NOT NULL,
        timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    ''')

    # Create unsuccessful_email_sends table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS unsuccessful_email_sends (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        success BOOLEAN NOT NULL,
        failure_reason TEXT,
        timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
    );
    ''')