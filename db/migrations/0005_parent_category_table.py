def up(cur):
    """Creates the parent_category_hierarchy table if it doesn't exist."""
    cur.execute('''
        CREATE TABLE IF NOT EXISTS parent_category_hierarchy
        (id SERIAL PRIMARY KEY,
        parent_category TEXT NOT NULL,
        category_order INTEGER UNIQUE NOT NULL);
    ''')
