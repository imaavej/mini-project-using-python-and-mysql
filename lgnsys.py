import mysql.connector
import getpass
import logging

logging.basicConfig(filename='upi_system.log', level=logging.INFO)

def get_mysql_pass():
    while True:
        mysql_pass=getpass,getpass("Enter Password: ")
        try:
            connection=mysql.connector.connect(
                 host="localhost",
                user="root",
                password=mysql_pass
            )
            connection.close()
            return mysql_pass
        except mysql.connector.Error as err:
            logging.error(f"MySQL Connection Error: {err}.")
            print(f"Error: {err}. Please try again.")

def get_connection(mysql_pass):
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password=get_mysql_pass,
        database='upi_system',
        autocommit=False
    )        

    cursor = connection.cursor()

    # Check if the database exists
    cursor.execute("SHOW DATABASES LIKE 'upi_system'")
    result = cursor.fetchone()

    if not result:
        # Create the 'upi_system' database
        cursor.execute("CREATE DATABASE upi_system")

        # Switch to the 'upi_system' database
        cursor.execute("USE upi_system")

        # Create the 'users' and 'transactions' tables
        create_users_table_query = (
            "CREATE TABLE IF NOT EXISTS users ("
            "user_id INT AUTO_INCREMENT PRIMARY KEY,"
            "username VARCHAR(255) NOT NULL UNIQUE,"
            "balance DECIMAL(10, 2) DEFAULT 0.0, password varchar(20))"
        )

        create_transactions_table_query = (
            "CREATE TABLE IF NOT EXISTS transactions ("
            "transaction_id INT AUTO_INCREMENT PRIMARY KEY,"
            "sender_id INT NOT NULL,"
            "receiver_id INT NOT NULL,"
            "amount DECIMAL(10, 2) NOT NULL,"
            "timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,"
            "FOREIGN KEY (sender_id) REFERENCES users(user_id),"
            "FOREIGN KEY (receiver_id) REFERENCES users(user_id))"
        )

        cursor.execute(create_users_table_query)
        cursor.execute(create_transactions_table_query)

        print("\ndatabase and tables created")

    cursor.close()
    connection.close()

def sign_up():
    username=input("Enter Username: ")
    password=input("Enter Password")

    connection=get_connection(mysql_pass)

while True:
    print("\nOptions:")
    print("1. Sign Up")
    print("2. Log In")
    print("3. exit ")

    choice=input("Enter your choice (1-3): ")

    if choice == '1' :

