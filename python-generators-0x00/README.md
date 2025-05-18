# Python Generators - MySQL Database Streaming

This project demonstrates how to use Python generators to stream rows from a MySQL database one by one.

## Files

- `seed.py`: Contains functions to set up and seed a MySQL database
- `0-main.py`: Main script to test the database setup and seeding

## Functions in seed.py

- `connect_db()`: Connects to the MySQL database server
- `create_database(connection)`: Creates the database ALX_prodev if it does not exist
- `connect_to_prodev()`: Connects to the ALX_prodev database in MySQL
- `create_table(connection)`: Creates a table user_data if it does not exist with the required fields
- `insert_data(connection, data)`: Inserts data in the database if it does not exist
- `row_generator(connection, batch_size=10)`: Generator function that yields rows from the database one by one

## Database Schema

The `user_data` table has the following fields:
- `user_id` (Primary Key, UUID, Indexed)
- `name` (VARCHAR, NOT NULL)
- `email` (VARCHAR, NOT NULL)
- `age` (DECIMAL, NOT NULL)

## Usage

1. Make sure you have MySQL installed and running
2. Update the database connection parameters in `seed.py` if needed
3. Run the main script:

```bash
python3 0-main.py