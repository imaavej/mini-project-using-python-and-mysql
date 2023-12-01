# mini-project-using-python-and-mysql

Student Management System
This is a simple student management system written in Python using MySQL as the database. 
It allows you to create, read, update, and delete students from a 'students' table in the 'student_management' database.

Features:

Create, read, update, and delete students
Input validation for student data
Error handling and logging
Uses MySQL database

Requirements:

Python 3 or higher
MySQL database server running
MySQL Connector Python library installed

Instructions:
Install the MySQL Connector Python library using pip:

Bash
pip install mysql-connector

Set up environment variables for MySQL connection:
MYSQL_USER: Your MySQL username
MYSQL_HOST: Your MySQL hostname (usually 'localhost')
MYSQL_DB: The name of your MySQL database ('student_management')
Save the provided Python script as student_management.py and run it:
Bash
python student_management.py

Follow the instructions on the screen to manage students.
Example Usage:

Create a student:
Enter student name: John Doe
Enter student email: jaunnelia@gmail.com
Enter student age: 25
Student created successfully!
Read students:
Students:
(1, 'Jaun Elia', 'jaunelia@gmail.com', 25)
Update a student:
Enter student ID to update: 1
Enter new student name: Faiz Ahmed
Enter new student email: faizahmed@gmail.com
Enter new student age: 30
Student updated successfully!
Delete a student:
Enter student ID to delete: 1
Student deleted successfully!
