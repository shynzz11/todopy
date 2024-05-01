from flask import Flask, request, jsonify
import json
import fsspec
#from requests_aws4auth import AWS4Auth  # Import AWS4Auth instead of AWSAuth
import pymysql
import base64
import hashlib

app = Flask(__name__)

# S3 bucket name
BUCKET_NAME = 'todobuckets3'

# Create fsspec filesystem object with AWS4Auth
s3 = fsspec.filesystem('s3', anon=False, key='AWS_KEY', secret='SECRET_AWS')

# Replace with your database connection logic (using libraries like SQLAlchemy)
todos = {}  # Temporary storage, replace with database interaction

@app.route('/users/<username>/todos', methods=['GET', 'POST'])
def user_todos(username):
    if request.method == 'GET':
        # Load todos from S3 (if file exists)
        try:
            s3_key = f"{username}_todos.json"
            with s3.open(f"{BUCKET_NAME}/{s3_key}", "r") as f:
                todos[username] = json.load(f)
        except FileNotFoundError:
            # Handle case where user's todo file doesn't exist
            todos[username] = []

        # Return user's todo list even after potential update from S3
        return jsonify(todos.get(username, []))

    elif request.method == 'POST':
        data = request.get_json()
        new_todo = data.get('todo')
        todos.setdefault(username, []).append(new_todo)  # Add new todo

        # Save todos to S3 bucket
        s3_key = f"{username}_todos.json"
        with s3.open(f"{BUCKET_NAME}/{s3_key}", "w") as f:
            json.dump(todos[username], f)

        return jsonify({'message': 'Todo added successfully!'})
    
def hash_password(password):
    """Hashes the password using SHA-256 and encodes it in Base64."""
    hash_object = hashlib.sha256(password.encode())
    hash_base64 = base64.b64encode(hash_object.digest()).decode()
    return hash_base64

def authenticate_from_database(username, password):
    try:
        # Connect to the SQL database
        hostdb = 'host'
        userdb = 'host'
        passworddb = '3'
        databasedb = 'b'
        connectiondb = pymysql.connect(
            host=hostdb,
            user=userdb,
            password=passworddb,
            database=databasedb
        )
        
        # Create a cursor object to execute SQL queries
        cursor = connectiondb.cursor()
        
        # Execute a query to check if the username and password are valid
        cursor.execute('SELECT * FROM users WHERE username=%s AND password_hash=%s', (username, password))
        
        # Fetch the first row from the result set
        user = cursor.fetchone()
        
        # Close the cursor and database connection
        cursor.close()
        connectiondb.close()
        
        # If user is found, return True; otherwise, return False
        if user:
            return True
        else:
            return False
    
    except Exception as e:
        # Print the error message and return False
        print(f"Error occurred: {e}")
        return False

# Start Flask application if authentication is successful
def start_flask_app(username, password):
    if authenticate_from_database(username, password):
        app.run(debug=True)
    else:
        print("Authentication failed. Flask application not started.")

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    password = hash_password(password)
    print(password)

    if username and password:
        # Perform authentication logic (e.g., call a function to check credentials)
        if authenticate_from_database(username, password):  # Replace with your authentication logic
            return jsonify({'message': 'Authentication successful.'})
        else:
            return jsonify({'error': 'Invalid username or password.'}), 401
    else:
        return jsonify({'error': 'Invalid username or password.'}), 401

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    try: 
        if username and password:
            # Hash the password before storing it in the database
            password_hash = hash_password(password)
            # Connect to the SQL database
            hostdb = 'm'
            userdb = 's'
            passworddb = 's'
            databasedb = 's'
            connectiondb = pymysql.connect(
                host=hostdb,
                user=userdb,
                password=passworddb,
                database=databasedb
            )
            
            # Create a cursor object to execute SQL queries
            cursor = connectiondb.cursor()
            
            # Execute a parameterized query to insert values into the database
            sql = "INSERT INTO users (username, password_hash) VALUES (%s, %s)"
            cursor.execute(sql, (username, password_hash))
            
            # Commit the transaction to save changes to the database
            connectiondb.commit()
            
            # Close the cursor and database connection
            cursor.close()
            connectiondb.close()
            
            return jsonify({'message': 'User created successfully.'})
        else:
            return jsonify({'error': 'Invalid username or password.'}), 400
    except Exception as e:
        # Print the error message and return an error response
        print(f"Error occurred: {e}")
        return jsonify({'error': 'An error occurred while creating the user.'}), 500

        
        
        
if __name__ == '__main__':
    
    app.run(debug=True)

