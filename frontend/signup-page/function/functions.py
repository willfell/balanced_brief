# import json
# import boto3
# import os
# import psycopg2

# # Initialize a session using Amazon Secrets Manager
# session = boto3.session.Session()
# client = session.client(
#     service_name='secretsmanager',
#     region_name='us-west-1'
# )

# secret_name = "bb/config-local"
# response = client.get_secret_value(SecretId=secret_name)
# secret_dict = json.loads(response['SecretString'])


# # print(secret_dict)
# #DB_PASS = secret_dict['POSTGRES_DB_PASS']
# DB_PASS = "db_pass"
# #DB_HOST = secret_dict['POSTGRES_DB_HOST']
# DB_HOST = "127.0"
# DB_USER = 'db_user'
# DB_NAME = 'postgres'
# DB_PORT = '5432'
# def connect_to_db():
#     return psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASS)
# conn = connect_to_db()
# cur = conn.cursor()
# print('made it')

# def check_for_duplicate_user(event):
#     # Prepare the SQL query to check for existing email
#     query = 'SELECT * FROM users WHERE email = %s;'

#     # Execute the query with the provided email
#     cur.execute(query, (event,))

#     # Fetch the result
#     result = cur.fetchone()

#     # Return True if a user with the given email exists, None otherwise
#     return True if result else None
