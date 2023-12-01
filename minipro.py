import mysql.connector
from decouple import config
import re
import getpass
import logging

# Setup logging
logging.basicConfig(filename='student_management.log', level=logging.INFO)

# Load environment variables
MYSQL_USER = config('MYSQL_USER', default='root')
MYSQL_HOST = config('MYSQL_HOST', default='localhost')
MYSQL_DB = config('MYSQL_DB', default='student_management')

# Function to prompt user for MySQL password
def get_mysql_password():
    while True:
        password = getpass.getpass("Enter MySQL password: ")
        try:
            connection = mysql.connector.connect(
                host=MYSQL_HOST,
                user=MYSQL_USER,
                password=password
            )
            connection.close()
            return password
        except mysql.connector.Error as err:
            logging.error(f"MySQL Connection Error: {err}.")
            print(f"Error: {err}. Please try again.")

# Function to establish a MySQL connection
def get_connection(password):
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=password,
        database=MYSQL_DB
    )

# Function to create a student table
def create_students_table(cursor):
    create_table_query = (
        "CREATE TABLE IF NOT EXISTS students ("
        "id INT AUTO_INCREMENT PRIMARY KEY,"
        "name VARCHAR(255) NOT NULL,"
        "email VARCHAR(255) NOT NULL,"
        "age INT)"
    )

    cursor.execute(create_table_query)
    logging.info("Students table created.")

# Function to check if the database exists, and create it if not
def create_database(password):
    connection = mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=password
    )
    
    cursor = connection.cursor()

    # Check if the database exists
    cursor.execute(f"SHOW DATABASES LIKE '{MYSQL_DB}'")
    result = cursor.fetchone()

    if not result:
        # Create the 'student_management' database
        cursor.execute(f"CREATE DATABASE {MYSQL_DB}")

    connection.commit()
    cursor.close()
    connection.close()

    # Establish a connection to the created database
    connection = get_connection(password)
    cursor = connection.cursor()

    # Create the 'students' table
    create_students_table(cursor)

    cursor.close()
    connection.close()

# Input validation functions
def is_valid_name(name):
    return bool(re.match("^[a-zA-Z\s]+$", name))

def is_valid_email(email):
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def is_valid_age(age):
    return age.isdigit()

# Function to create a student
def create_student(password):
    connection = get_connection(password)
    cursor = connection.cursor()

    while True:
        name = input("Enter student name: ")
        if not is_valid_name(name):
            print("Invalid name. Please enter a valid name.")
            continue
        else:
            break

    while True:
        email = input("Enter student email: ")
        if not is_valid_email(email):
            print("Invalid email. Please enter a valid email.")
            continue
        else:
            break

    while True:
        age = input("Enter student age: ")
        if not is_valid_age(age):
            print("Invalid age. Please enter a valid age.")
            continue
        else:
            break

    try:
        # Insert student into the 'students' table in a transaction
        insert_query = "INSERT INTO students (name, email, age) VALUES (%s, %s, %s)"
        student_data = (name, email, int(age))

        cursor.execute(insert_query, student_data)
        connection.commit()

        print("Student created successfully!")
    except mysql.connector.Error as err:
        connection.rollback()
        logging.error(f"MySQL Error: {err}")
        print(f"Error creating student: {err}")
    finally:
        cursor.close()
        connection.close()

# Function to read students
def read_students(password):
    connection = get_connection(password)
    cursor = connection.cursor()

    try:
        # Select all students from the 'students' table
        select_query = "SELECT * FROM students"
        cursor.execute(select_query)
        students = cursor.fetchall()

        if not students:
            print("No students found.")
        else:
            print("Students:")
            for student in students:
                print(student)
    except mysql.connector.Error as err:
        logging.error(f"MySQL Error: {err}")
        print(f"Error reading students: {err}")
    finally:
        cursor.close()
        connection.close()

# Function to update a student
def update_student(password):
    connection = get_connection(password)
    cursor = connection.cursor()

    student_id = int(input("Enter student ID to update: "))
    new_name = input("Enter new student name: ")
    new_email = input("Enter new student email: ")
    new_age = input("Enter new student age: ")

    # Input validation for update
    if not is_valid_name(new_name) or not is_valid_email(new_email) or not is_valid_age(new_age):
        print("Invalid input. Please enter valid data for updating the student.")
        return

    try:
        # Update the name, age, and email of a specific student in a transaction
        update_query = "UPDATE students SET name = %s, age = %s, email = %s WHERE id = %s"
        update_data = (new_name, int(new_age), new_email, student_id)

        cursor.execute(update_query, update_data)
        connection.commit()

        if cursor.rowcount == 0:
            print(f"Student with ID {student_id} not found.")
        else:
            print("Student updated successfully!")
    except mysql.connector.Error as err:
        connection.rollback()
        logging.error(f"MySQL Error: {err}")
        print(f"Error updating student: {err}")
    finally:
        cursor.close()
        connection.close()

# Function to delete a student
def delete_student(password):
    connection = get_connection(password)
    cursor = connection.cursor()

    student_id = int(input("Enter student ID to delete: "))

    try:
        # Delete a specific student in a transaction
        delete_query = "DELETE FROM students WHERE id = %s"
        delete_data = (student_id,)

        cursor.execute(delete_query, delete_data)
        connection.commit()

        if cursor.rowcount == 0:
            print(f"Student with ID {student_id} not found.")
        else:
            print("Student deleted successfully!")
    except mysql.connector.Error as err:
        connection.rollback()
        logging.error(f"MySQL Error: {err}")
        print(f"Error deleting student: {err}")
    finally:
        cursor.close()
        connection.close()

# Get MySQL password from user
mysql_password = get_mysql_password()

# Check and create database
create_database(mysql_password)

while True:
    print("\nOptions:")
    print("1. Create Student")
    print("2. Read Students")
    print("3. Update Student")
    print("4. Delete Student")
    print("5. Exit")

    choice = input("Enter your choice (1-5): ")

    if choice == '1':
        create_student(mysql_password)
    elif choice == '2':
        read_students(mysql_password)
    elif choice == '3':
        update_student(mysql_password)
    elif choice == '4':
        delete_student(mysql_password)
    elif choice == '5':
        print("Exiting program. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")
