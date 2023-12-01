import mysql.connector
import getpass

# Function to prompt user for MySQL password
def get_mysql_password():
    while True:
        password = getpass.getpass("Enter MySQL password: ")
        try:
            # Try to establish a MySQL connection to check the password
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password=password
            )
            # If successful, close the connection and return the password
            connection.close()
            return password
        except mysql.connector.Error as err:
            # If there's an error (e.g., wrong password), prompt the user to try again
            print(f"Error: {err}. Please try again.")

# Function to establish a MySQL connection
def get_connection(password):
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password=password,
        database='upi_system',
        autocommit=False
    )

# Function to create the database and tables
def create_database(password):
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password=password
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
            "balance DECIMAL(10, 2) DEFAULT 0.0)"
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

# Function to perform a fund transfer
def transfer_funds(sender_id, receiver_id, amount, password):
    connection = get_connection(password)
    cursor = connection.cursor()

    try:
        # Begin the transaction
        cursor.execute("START TRANSACTION")

        # Check if the sender has sufficient balance
        cursor.execute("SELECT balance FROM users WHERE user_id = %s", (sender_id,))
        sender_balance = cursor.fetchone()[0]
        if sender_balance < amount:
            raise ValueError("Insufficient balance for the transfer.")

        # Update sender's balance
        cursor.execute("UPDATE users SET balance = balance - %s WHERE user_id = %s", (amount, sender_id))

        # Update receiver's balance
        cursor.execute("UPDATE users SET balance = balance + %s WHERE user_id = %s", (amount, receiver_id))

        # Insert a record into the transactions table
        cursor.execute("INSERT INTO transactions (sender_id, receiver_id, amount) VALUES (%s, %s, %s)",
                       (sender_id, receiver_id, amount))

        # Commit the transaction
        connection.commit()

        print("Transaction successful!")

    except mysql.connector.Error as err:
        print(f"Error: {err}. Rolling back changes.")
        connection.rollback()

    finally:
        cursor.close()
        connection.close()

# Function to check the balance of a user
def check_balance(user_id, password):
    connection = get_connection(password)
    cursor = connection.cursor()

    try:
        # Retrieve and display the user's balance
        cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
        user_balance = cursor.fetchone()
        if user_balance:
            print(f"User ID {user_id} balance: {user_balance[0]}")
        else:
            print(f"User with ID {user_id} not found.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        cursor.close()
        connection.close()

# Main program
mysql_password = get_mysql_password()

# Check and create the database and tables
create_database(mysql_password)

while True:
    print("\nOptions:")
    print("1. Transfer Funds")
    print("2. Check Balance")
    print("3. Exit")

    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        sender_id = int(input("Enter sender user ID: "))
        receiver_id = int(input("Enter receiver user ID: "))
        amount = float(input("Enter the amount to transfer: "))

        transfer_funds(sender_id, receiver_id, amount, mysql_password)

    elif choice == '2':
        user_id = int(input("Enter user ID to check balance: "))
        check_balance(user_id, mysql_password)

    elif choice == '3':
        print("Exiting program. Goodbye!")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 3.")
