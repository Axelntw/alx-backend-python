#!/usr/bin/python3
"""
Module for batch processing users from a MySQL database
"""
import mysql.connector


def stream_users_in_batches(batch_size):
    """
    Generator function that yields rows from the user_data table in batches
    
    Args:
        batch_size: Number of rows to fetch in each batch
        
    Returns:
        Generator yielding batches of rows
    """
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="ALX_prodev"
        )
        
        # Create a cursor
        cursor = connection.cursor(dictionary=True)
        
        # Execute the query
        cursor.execute("SELECT * FROM user_data")
        
        # Fetch and yield batches
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
            
        # Clean up
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as e:
        print(f"Error: {e}")
        yield []


def batch_processing(batch_size):
    """
    Processes each batch to filter users over the age of 25
    
    Args:
        batch_size: Number of rows to fetch in each batch
        
    Returns:
        List of filtered users over the age of 25
    """
    filtered_users = []
    
    # Get batches from the generator
    for batch in stream_users_in_batches(batch_size):
        # Process each user in the batch
        for user in batch:
            # Filter users over the age of 25
            if user['age'] > 25:
                print(user)
                print()  # Empty line after each user
                filtered_users.append(user)
    
    return filtered_users