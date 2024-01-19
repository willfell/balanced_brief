import json
import boto3
import os
import psycopg2
from psycopg2 import OperationalError
from datetime import datetime


# Initialize a session using Amazon Secrets Manager
session = boto3.session.Session()
client = session.client(service_name="secretsmanager", region_name="us-west-1")

secret_name = "bb/config"
response = client.get_secret_value(SecretId=secret_name)
secret_dict = json.loads(response["SecretString"])


DB_PASS = secret_dict["POSTGRES_DB_PASS"]
DB_HOST = secret_dict["POSTGRES_DB_HOST"]
DB_USER = "postgres"
DB_NAME = "postgres"
DB_PORT = "5432"


def connect_to_db():
    try:
        return psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            connect_timeout=10  # Timeout in seconds
        )
    except OperationalError as e:
        print(f"Failed to connect to DB: {e}")
        return None


print("Connecting to DB")
conn = connect_to_db()
cur = conn.cursor()


def check_for_duplicate_user(requestor):
    # Prepare the SQL query to check for existing email
    query = "SELECT * FROM users WHERE email = %s;"

    # Execute the query with the provided email
    cur.execute(query, (requestor["email"],))

    # Fetch the result
    result = cur.fetchone()

    # Return True if a user with the given email exists, None otherwise
    return True if result else None


def add_user_to_db(requestor):
    query = """INSERT INTO users (email, first_name, last_name, interests, date_of_birth, verified)
               VALUES (%s, %s, %s, %s, %s, %s);"""

    # Extract user data from the requestor object
    email = requestor.get("email").lower()
    first_name = requestor.get("firstName").title()
    last_name = requestor.get("lastName").title()
    interests = requestor.get("newsSelected", [])
    print("Here are the interests that are being inserted")
    print(interests)
    date_of_birth = requestor.get("dateOfBirth")
    verified = False  # default value, as per your table structure

    # Execute the query
    try:
        cur.execute(query, (email, first_name, last_name, interests, date_of_birth, verified))
        conn.commit()  # Commit the transaction
        print("User added successfully.")
        return True
    except Exception as e:
        print("Error adding user:", e)
        conn.rollback()  # Rollback in case of error
        return False


def update_user_verification(requestor):
    query = """UPDATE users 
               SET verified = %s, verified_at = %s 
               WHERE email = %s;"""

    # Current timestamp
    current_timestamp = datetime.now()

    # Execute the query
    try:
        cur.execute(query, (True, current_timestamp, requestor.lower()))
        conn.commit()  # Commit the transaction
        print("User verified successfully.")
        return True
    except Exception as e:
        print("Error verifying user:", e)
        conn.rollback()  # Rollback in case of error
        return False

def check_user_and_unsubscribe(email):
    try:
        with conn.cursor() as cur:
            # Check if user exists
            cur.execute("SELECT unsubscribed FROM users WHERE email = %s", (email,))
            result = cur.fetchone()

            if result is None:
                # User does not exist
                return False, {"status": "error", "message": f"{email} does not exist"}

            is_unsubscribed = result[0]
            if is_unsubscribed:
                # User already unsubscribed
                return False, {"status": "error", "message": f"{email} already unsubscribed"}

            # Unsubscribe the user
            cur.execute("UPDATE users SET unsubscribed = TRUE, unsubscribed_at = %s WHERE email = %s", (datetime.now(), email))
            conn.commit()

            return True, {"status": "success", "message": "User successfully unsubscribed"}

    except psycopg2.Error as e:
        # Handle database errors
        print("Database error:", e)
        return False, {"status": "error", "message": "Database error"}

    finally:
        conn.close()


