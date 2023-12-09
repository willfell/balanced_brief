import psycopg2
import importlib
import os
import boto3
import json
client = boto3.client('secretsmanager')
secret_name = "bb/config"
response = client.get_secret_value(SecretId=secret_name)
if 'SecretString' in response:
    secret = response['SecretString']
else:
    binary_secret_data = response['SecretBinary']
secret_dict = json.loads(secret)

DB_PASS = secret_dict['POSTGRES_DB_PASS']
DB_HOST = secret_dict['POSTGRES_DB_HOST']
# DB_PASS = os.environ['POSTGRES_DB_PASS']
# DB_HOST = os.environ['POSTGRES_DB_HOST']
DB_USER = 'db_user'
DB_NAME = 'postgres'
DB_PORT = '5432'

def connect_to_db():
    return psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASS)

def create_migration_table_if_not_exists(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS migrations (version INTEGER PRIMARY KEY);''')

def get_applied_migrations(cur):
    cur.execute('''SELECT version FROM migrations ORDER BY version ASC;''')
    return {row[0] for row in cur.fetchall()}

def main():
    conn = connect_to_db()
    cur = conn.cursor()

    create_migration_table_if_not_exists(cur)

    applied_versions = get_applied_migrations(cur)
    migrations_to_apply = set(range(1, 10001))  # Assuming a max of 1000 migrations for this example



    for version in sorted(migrations_to_apply - applied_versions):
        
        migration_map = {
            1: "create_users",
            2: "insert_users",
            3: "create_subreddits_table",
            4: "insert_subreddits",
            5: "parent_category_table",
            6: "insert_parent_categories",
            7: "create_posts_tables",
            8: "create_email_send_log_tables"
        }

        if version in migration_map:
            print("===================================")
            migration_name = migration_map[version]
            print(f"Migration Name = {migration_name}")
            migration = importlib.import_module(f"migrations.{str(version).zfill(4)}_{migration_name}")
            migration.up(cur)
            cur.execute("INSERT INTO migrations (version) VALUES (%s);", (version,))
        conn.commit()
    print("Migrations Complete")
    print("===============================")


if __name__ == "__main__":
    main()
