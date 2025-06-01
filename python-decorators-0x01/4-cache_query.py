import time
import sqlite3
import functools
from typing import Callable, Any, Dict

# Global cache dictionary
query_cache: Dict[str, Any] = {}

def with_db_connection(func: Callable) -> Callable:
    """Decorator that handles database connection automatically."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

def cache_query(func: Callable) -> Callable:
    """
    Decorator that caches query results based on the query string.
    Returns cached result if query was executed before.
    """
    @functools.wraps(func)
    def wrapper(conn, query: str, *args, **kwargs):
        if query in query_cache:
            print(f"Cache hit for query: {query}")
            return query_cache[query]
        
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        print(f"Cache miss for query: {query}")
        return result
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

if __name__ == "__main__":
    # First call will cache the result
    users = fetch_users_with_cache(query="SELECT * FROM users")
    
    # Second call will use the cached result
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
