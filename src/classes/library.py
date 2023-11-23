""" ABC module => Abstract Base Class """
from abc import ABC, abstractmethod


class Library(ABC):
    """ Abstract class will define 'what' not 'how'
        - Will have method signatures for required operations
        - Will not have any code implementations
        - Used as a blueprint
    """
    @abstractmethod
    def is_table_exists(self, table_name):
        """ Function to check if the database contains 'specified' table """

    @abstractmethod
    def is_table_empty(self, table_name):
        """ Function to check if 'specified' table is empty or has data """

    @abstractmethod
    def is_value_in_table(self, table_name, column_name, value):
        """ Function to check if 'specified' column in table has 'specified' value """

    @abstractmethod
    def num_total_rows(self, table_name):
        """ Functions to count and return total number of rows in table """

    @abstractmethod
    def get_id(self, table_name, column_name, value):
        """ Function to extract id """

    @abstractmethod
    def fetch_all_records(self, table_name, is_headers_included):
        """ Function to fetch all records in 'specified' table with headers if required  """

    @abstractmethod
    def fetch_record(self, table_name, column_name, value, is_headers_included):
        """ Function to fetch a single record in 'specified' table with headers if required """

    @abstractmethod
    def fetch_books_by_author(self, author_name, is_headers_included):
        """ Function to fetch books written by 'specified' author """

    @abstractmethod
    def update_record(self, table_name, column_name, record_id, value):
        """ Function to update 'column_name' in 'table_name' with 'value' """

    @abstractmethod
    def delete_record(self, table_name, id_num):
        """ Function to delete entire row from table_name where id = id_num """
