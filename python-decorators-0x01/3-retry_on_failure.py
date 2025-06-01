import time
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
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

def retry_on_failure(retries: int = 3, delay: int = 2) -> Callable:
    """
    Decorator that retries a function if it fails.
    Args:
        retries: Number of retry attempts
        delay: Delay between retries in seconds
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == retries - 1:  # Last attempt
                        raise e
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

if __name__ == "__main__":
    users = fetch_users_with_retry()
    print(users)
