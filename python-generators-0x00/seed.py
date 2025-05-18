#!/usr/bin/python3
"""
Module for setting up and seeding a MySQL database
"""
import mysql.connector
import csv
import os
from mysql.connector import Error


def connect_db():
    """
    Connects to the MySQL database server
    Returns: MySQL connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=""
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None


def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist
    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")


def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL
    Returns: MySQL connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None


def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields
    Args:
        connection: MySQL connection object
    """
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            )
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except Error as e:
        print(f"Error creating table: {e}")


def insert_data(connection, csv_file):
    """
    Inserts data in the database if it does not exist
    Args:
        connection: MySQL connection object
        csv_file: Path to the CSV file containing user data
    """
    try:
        # Check if file exists
        if not os.path.exists(csv_file):
            print(f"Error: File {csv_file} not found")
            return

        cursor = connection.cursor()
        
        # Read CSV file and insert data
        with open(csv_file, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            
            for row in csv_reader:
                # Check if record already exists
                cursor.execute(
                    "SELECT COUNT(*) FROM user_data WHERE user_id = %s",
                    (row[0],)
                )
                count = cursor.fetchone()[0]
                
                if count == 0:
                    # Insert new record
                    cursor.execute(
                        "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)",
                        (row[0], row[1], row[2], row[3])
                    )
        
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")


def row_generator(connection, batch_size=10):
    """
    Generator function that yields rows from the database one by one
    Args:
        connection: MySQL connection object
        batch_size: Number of rows to fetch at once (for efficiency)
    Yields:
        One row at a time from the user_data table
    """
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")
        
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            
            for row in rows:
                yield row
                
        cursor.close()
    except Error as e:
        print(f"Error in row generator: {e}")
        yield None