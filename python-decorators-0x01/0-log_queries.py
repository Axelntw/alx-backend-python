import sqlite3
import functools
from typing import Callable

def log_queries() -> Callable:
    """
    Decorator that logs SQL queries before execution.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Extract query from args or kwargs
            query = args[0] if args else kwargs.get('query')
            # Log the query
            print(f"Query: {query}")
            # Execute the original function
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_queries()
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

if __name__ == "__main__":
    # Example usage
    users = fetch_all_users(query="SELECT * FROM users")