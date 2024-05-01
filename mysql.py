import pymysql

# Replace these values with your MySQL database credentials
host = 'host'
user = 'host'
password = 'host'
database = 'host'

# Establish a connection to the MySQL server
try:
    connection = pymysql.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    cursor = connection.cursor()

    # Define the SQL stat'ement to create the users table
    #create_table_query = "DROP TABLE IF EXISTS users"
    create_table_query = "SELECT * FROM  users"


    # Execute the SQL statement to create the table
    cursor.execute(create_table_query)
    results = cursor.fetchall()  # Fetch all rows

    # Print each row or relevant data from results
    for row in results:
        print(row)  # Prints each row as a tuple
        print("Table 'users' created successfully!")

except pymysql.Error as error:
    print("Failed to connect to MySQL server:", error)

finally:
    # Close the cursor and connection
    if 'connection' in locals() and connection.open:
        cursor.close()
        connection.close()
        print("MySQL connection closed.")
