#!/usr/bin/python3
"""
Module for streaming users from a MySQL database
"""
import mysql.connector


def stream_users():
    """
    Generator function that yields rows from the user_data table one by one
    
    Returns:
        Generator yielding one row at a time as a dictionary
    """
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        
        # Create a cursor that returns dictionaries
        cursor = connection.cursor(dictionary=True)
        
        # Execute the query
        cursor.execute("SELECT * FROM user_data")
        
        # Yield rows one by one
        for row in cursor:
            yield row
            
        # Clean up
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        yield None