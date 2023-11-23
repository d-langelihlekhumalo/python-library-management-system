""" Module imports """
import sqlite3
from src.classes import library
from . import utilities

_database_path = utilities.get_database_path()


class DatabaseOperations(library.Library):
    """ Class to perform varies database related operations """

    def is_table_exists(self, table_name):
        """ Function to check if table exists in database """
        table_exists = False
        try:
            with sqlite3.connect(_database_path) as connection:
                cursor = connection.cursor()
                sql_query = f"SELECT * FROM {table_name}"
                cursor.execute(sql_query)
                table_exists = cursor.fetchall() is not None

                return table_exists
        except sqlite3.DatabaseError:
            return table_exists

    def is_table_empty(self, table_name):
        """ Function to check if table has any data """
        try:
            with sqlite3.connect(_database_path) as connection:
                cursor = connection.cursor()
                command = f"SELECT COUNT(*) FROM {table_name}"
                cursor.execute(command)
                # Fetch the first column value
                row_count = cursor.fetchone()[0]

                return row_count < 1  # Return True if row_count is greater than 0

        except sqlite3.DatabaseError:
            return False

    def is_value_in_table(self, table_name, column_name, value):
        """ Function to check if record exists in table_name """
        try:
            with sqlite3.connect(_database_path) as connection:
                cursor = connection.cursor()
                command = f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} COLLATE NOCASE = ?"
                cursor.execute(command, (value,))
                count = cursor.fetchone()[0]

                return bool(count > 0)

        except sqlite3.DatabaseError:
            return False

    def num_total_rows(self, table_name):
        """ Functions to count and return total number of rows in table """
        try:
            with sqlite3.connect(_database_path) as connection:
                cursor = connection.cursor()
                command = f"SELECT COUNT(*) FROM {table_name};"
                cursor.execute(command)
                count = cursor.fetchone()[0]

                return count if count > 0 else 0

        except sqlite3.DatabaseError as error:
            return utilities.database_operational_error(error)

    def get_id(self, table_name, column_name, value):
        """ Function to extract id from table """
        if self.is_value_in_table(table_name, column_name, value):
            try:
                with sqlite3.connect(_database_path) as connection:

                    cursor = connection.cursor()
                    sql_query = f"""SELECT id FROM {table_name} WHERE {column_name} COLLATE NOCASE = ?;"""
                    cursor.execute(sql_query, (value,))

                    records = cursor.fetchall()[0]
                    return records[0]

            except sqlite3.DatabaseError as error:
                return utilities.database_operational_error(error)
        return -1

    def fetch_all_records(self, table_name, is_headers_included):
        """ Function to return all records from a table """
        try:
            with sqlite3.connect(_database_path) as connection:
                cursor = connection.cursor()
                cursor.execute(
                    utilities.sanitize_sql_command(table_name) + ";")
                records = cursor.fetchall()
                # Check if records must be tabulated
                if not is_headers_included:
                    return records

                headers = [description[0]
                           for description in cursor.description]
                return utilities.tabulate_extracted_records(headers, records)

        except sqlite3.DatabaseError as error:
            return utilities.database_operational_error(error)

    def fetch_record(self, table_name, column_name, value, is_headers_included):
        """ Function to return record from a table_name """
        if self.is_value_in_table(table_name, column_name, value):
            try:
                with sqlite3.connect(_database_path) as connection:

                    cursor = connection.cursor()
                    statement = utilities.sanitize_sql_command(
                        table_name) + f" WHERE {column_name} COLLATE NOCASE = ?;"

                    cursor.execute(statement, (value,))

                    records = cursor.fetchall()
                    # Check if records must be tabulated
                    if len(records) > 0:
                        if not is_headers_included:
                            return records

                        headers = [description[0]
                                   for description in cursor.description]
                        return utilities.tabulate_extracted_records(headers, records)

            except sqlite3.DatabaseError as error:
                return utilities.database_operational_error(error)
        return f"Sorry, but we currently don't have any {table_name}s with {column_name}: {value} in stock."

    def fetch_books_by_author(self, author_name, is_headers_included):
        """ Function to return records from a table """
        try:
            with sqlite3.connect(_database_path) as connection:
                cursor = connection.cursor()
                # Get author's ID based on the provided name
                sql_author_query = "SELECT id FROM author WHERE full_name COLLATE NOCASE = ?"
                cursor.execute(sql_author_query, (author_name,))
                author_id = cursor.fetchone()

                if author_id:
                    if self.is_value_in_table('book', 'author_id', author_id[0]):
                        # Get books by the author using the author's ID
                        sql_query = """
                        SELECT book.title, book.isbn, author.full_name AS author_name
                        FROM book
                        JOIN author ON book.author_id = author.id
                        WHERE author_id = ?
                        """
                        cursor.execute(sql_query, author_id)
                        books = cursor.fetchall()

                        # Check if records must be tabulated
                        if not is_headers_included:
                            return books

                        headers = [description[0]
                                   for description in cursor.description]
                        return utilities.tabulate_extracted_records(headers, books)
                    return f"Author {author_name} currently has no books"
                return f"Author {author_name} not found in the database."

        except sqlite3.DatabaseError as error:
            return utilities.database_operational_error(error)

    def update_record(self, table_name, column_name, record_id, value):
        """ Function to update 'column_name' in 'table_name' with 'value' """
        try:
            with sqlite3.connect(_database_path) as connection:
                update_infor = (value, record_id)
                cursor = connection.cursor()
                query = f"UPDATE {table_name} SET {column_name} = ? WHERE id = ?"
                cursor.execute(query, update_infor)
                connection.commit()
            return True
        except sqlite3.DatabaseError as error:
            return utilities.database_operational_error(error=error)

    def delete_record(self, table_name, id_num):
        """ Function to delete entire row from table_name where id = id_num """
        try:
            with sqlite3.connect(_database_path) as connection:
                cursor = connection.cursor()
                query = f"DELETE FROM {table_name} WHERE id = ?"
                cursor.execute(query, (id_num,))
                connection.commit()
            return True
        except sqlite3.DatabaseError as error:
            return utilities.database_operational_error(error=error)
