import pymysql
import base64
import hashlib

# Replace these values with your MySQL database credentials
host = 'host'
user = 'host
password = 'host'
database = 'host'

def hash_password(password):
    """Hashes the password using SHA-256 and encodes it in Base64."""
    hash_object = hashlib.sha256(password.encode())
    hash_base64 = base64.b64encode(hash_object.digest()).decode()
    return hash_base64

# Establish a connection to the MySQL server
try:
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()

    # Define the SQL statement to create the users table if it does not exist
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password_hash VARCHAR(255) NOT NULL
    )
    """

    # Execute the SQL statement to create the table
    cursor.execute(create_table_query)
    print("Table 'users' created successfully!")


    # Sample username and password
    username = 'syan'
    password = 'syan'

    # Hash the password and encode it in Base64
    password_hash = hash_password(password)

    # Define the SQL statement to insert a user into the users table
    insert_user_query = """
    INSERT INTO users (username, password_hash) VALUES (%s, %s)
    """

    # Execute the SQL statement to insert the user
    cursor.execute(insert_user_query, (username, password_hash))
    connection.commit()
    print(f"User '{username}' added successfully!")

except pymysql.Error as error:
    print("Failed to connect to MySQL server:", error)

finally:
    # Close the cursor and connection
    if 'connection' in locals() and connection.open:
        cursor.close()
        connection.close()
        print("MySQL connection closed.")
