import sqlite3
import functools
from typing import Callable, Any

def with_db_connection(func: Callable) -> Callable:
    """
    Decorator that handles database connection automatically.
    Opens connection before function execution and closes it afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Create database connection
        conn = sqlite3.connect('users.db')
        try:
            # Call the function with connection as first argument
            result = func(conn, *args, **kwargs)
            return result
        finally:
            # Ensure connection is always closed
            conn.close()
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

if __name__ == "__main__":
    # Example usage
    user = get_user_by_id(user_id=1)
    print(user)