import unittest
from tool_sql import DatabaseInstance  # Import your DatabaseInstance class from the correct module

class TestDatabaseInstance(unittest.TestCase):

    def test_create_random_table(self):
        # Initialize a DatabaseInstance object
        db_instance = DatabaseInstance()

        # Get a database cursor
        db_cursor = db_instance.get_db_cursor()

        # Define an SQL statement to create a random table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS random_data (
            id INT PRIMARY KEY,
            name VARCHAR(255),
            value INT
        )
        """

        try:
            # Execute the SQL statement to create the table
            db_cursor.execute(create_table_sql)

            # Commit the changes to the database
            db_instance.get_db_connection().commit()

            # Verify if the table exists
            db_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='random_data'")
            table_exists = db_cursor.fetchone() is not None

            # Assert that the table was created
            self.assertTrue(table_exists)

        finally:
            # Clean up: Drop the table after testing (optional)
            db_cursor.execute("DROP TABLE IF EXISTS random_data")
            db_instance.get_db_connection().commit()

    # Add more test methods as needed

if __name__ == '__main__':
    unittest.main()
