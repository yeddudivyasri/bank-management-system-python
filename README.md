~~~Bank Management System - Python Tkinter + MySQL

This is a GUI-based Bank Management System developed using Python, Tkinter, and MySQL.  
It was built as part of a 3-month internship at BDPS Pvt. Ltd. to understand real-time application development with database integration.


* Features

- User Login and Registration  
- Open Bank Account with Auto-generated Account Number  
- View Account Information  
- Deposit and Withdraw Money  
- Close Account (Permanent Delete)  
- Dashboard Navigation  
- GUI-based Application using Tkinter  


* Technologies Used

- Python 3  
- Tkinter for GUI  
- MySQL for Database  
- mysql-connector-python  


* Database Setup

1. Create a database named `bank_db` in MySQL.

2. Use the following SQL commands to create the required tables:

~~sql
CREATE TABLE users (
    full_name1 VARCHAR(100),
    email1 VARCHAR(100),
    phone1 VARCHAR(15),
    login_id VARCHAR(50) PRIMARY KEY,
    login_password VARCHAR(50)
);

CREATE TABLE accounts (
    account_no INT PRIMARY KEY,
    account_holder1 VARCHAR(100),
    address1 VARCHAR(200),
    address2 VARCHAR(200),
    email1 VARCHAR(100),
    dob1 DATE,
    balance1 FLOAT
);
How to Run
1. Clone this repository or download the source code.

2. Install the required Python package:
        pip install mysql-connector-python

3.  Ensure MySQL is running and the bank_db database is set up properly.

4.  Run the application using:
     python banking_app.py
