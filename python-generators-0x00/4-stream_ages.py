#!/usr/bin/python3
"""
Module for calculating average age using generators
"""
import mysql.connector


def stream_user_ages():
    """
    Generator function that yields user ages one by one
    
    Returns:
        Generator yielding user ages
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
        cursor = connection.cursor()
        
        # Execute the query to get only the age column
        cursor.execute("SELECT age FROM user_data")
        
        # Yield ages one by one
        for (age,) in cursor:
            yield age
            
        # Clean up
        cursor.close()
        connection.close()
        
    except mysql.connector.Error as e:
        print(f"Error: {e}")


def calculate_average_age():
    """
    Calculates the average age using the stream_user_ages generator
    
    Returns:
        Average age of all users
    """
    total_age = 0
    count = 0
    
    # Use the generator to process ages one by one
    for age in stream_user_ages():
        total_age += age
        count += 1
    
    # Calculate and return the average
    if count > 0:
        return total_age / count
    else:
        return 0


if __name__ == "__main__":
    # Calculate and print the average age
    avg_age = calculate_average_age()
    print(f"Average age of users: {avg_age:.2f}")