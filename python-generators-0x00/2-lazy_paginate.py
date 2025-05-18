#!/usr/bin/python3
"""
Module for lazy pagination of users from a MySQL database
"""
seed = __import__('seed')


def paginate_users(page_size, offset):
    """
    Fetches a page of users from the database
    
    Args:
        page_size: Number of rows to fetch in each page
        offset: Starting position for fetching rows
        
    Returns:
        List of user dictionaries for the requested page
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_pagination(page_size):
    """
    Generator function that lazily loads pages of users
    
    Args:
        page_size: Number of rows to fetch in each page
        
    Returns:
        Generator yielding one page at a time
    """
    offset = 0
    
    while True:
        # Fetch the next page
        page = paginate_users(page_size, offset)
        
        # If the page is empty, we've reached the end
        if not page:
            break
        
        # Yield the current page
        yield page
        
        # Update the offset for the next page
        offset += page_size