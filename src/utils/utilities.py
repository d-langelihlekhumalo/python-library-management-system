""" Module imports """
import os
import sys
import re
from pathlib import Path
from datetime import datetime
import random
from tabulate import tabulate


def get_current_date():
    """ Function to display current date """
    return datetime.now().strftime("%d/%m/%Y")


def _get_path(path_module, source):
    """ Function to return path to resources folder """
    return path_module(os.path.abspath(os.curdir) + source)


def get_database_path():
    """ Function to return database path """
    return _get_path(Path, "\\src\\resources\\library_management_system.sqlite3")


def is_valid_path(path_to_check):
    """ Function to check if path is valid """
    return os.path.exists(path_to_check)


def is_single_digit(input_str):
    "Check if input_str is single digit"
    return input_str.isdigit() and len(input_str) == 1


def is_valid_isbn(isbn):
    """ Function to check if book isbn is valid: digits & 13 characters """
    pattern = r'^\d{10}$|^\d{13}$'
    return bool(re.match(pattern, isbn))


def is_valid_input(input_str):
    """ Function to check if input_str is valid """
    pattern = r'^[A-Za-z]+ [A-Za-z]+$'
    return bool(re.match(pattern, input_str))


def is_valid_str(input_str):
    """ Function to check if input is valid str """
    return isinstance(input_str, str)


def format_to_title_case(input_str):
    """ Function to capitalize each word """
    words = input_str.split()  # Split the input string into words
    title_words = [word.capitalize() for word in words]
    return ' '.join(title_words)


def is_valid_option(input_str, min_value, max_value):
    "Check if input_str is a valid option"
    return int(input_str) >= int(min_value) and int(input_str) <= int(max_value)


def generate_random_num():
    """ Generate random number"""
    return random.randint(1, 10)


def get_full_name(entity):
    """ Function to return entity full name """
    full_name = ''
    while True:
        full_name = format_to_title_case(
            input(f"Enter {entity} full name: "))
        if is_valid_input(full_name):
            break
    return full_name


def is_table_exists(database_path, table_name, sqlite3_module):
    """ Function to check if table exists """
    table_exists = False
    try:
        with sqlite3_module.connect(database_path) as connection:
            cursor = connection.cursor()
            sql_query = f"SELECT * FROM {table_name}"
            cursor.execute(sql_query)
            table_exists = cursor.fetchall() is not None

            return table_exists
    except sqlite3_module.OperationalError:
        return table_exists


def database_operational_error(error):
    """ Function to return specific database error """
    return f"DatabaseError: {error}"


def _center_align_headers(headers, table):
    """ Private function to center align database table headers """
    col_widths = [max(len(str(row[i])) for row in table)
                  for i in range(len(headers))]
    centered_headers = [f"{header:^{width}}" for header,
                        width in zip(headers, col_widths)]
    return centered_headers


def sanitize_sql_command(table_name):
    """ Function to sanitize sql command """
    sanitized_statement = ''
    match table_name:
        case 'author':
            sanitized_statement = """
            SELECT author.full_name AS "author name", author.country
            FROM author"""
        case 'book':
            sanitized_statement = """
            SELECT book.isbn, book.title, author.full_name AS "author name", 
            stock.quantity AS total, stock.leased, stock.quantity - stock.leased AS available
            FROM book
            JOIN author ON book.author_id = author.id
            JOIN stock ON book.id = stock.book_id"""
        case 'borrowed_book':
            sanitized_statement = """
            SELECT book.isbn, book.title, author.full_name AS "author name",
            checkout.quantity, checkout.checkout_date,
            checkout.status, checkout.return_date
            FROM borrowed_book
            JOIN book ON borrowed_book.book_id = book.id
            JOIN author ON book.author_id = author.id
            JOIN checkout ON borrowed_book.checkout_id = checkout.id"""
        case 'checkout':
            sanitized_statement = """
            SELECT book.isbn, book.title, author.full_name AS "author name",
            checkout.quantity, checkout.checkout_date, checkout.status, checkout.return_date
            FROM checkout
            JOIN book ON checkout.book_id = book.id
            JOIN author ON book.author_id = author.id"""
        case 'stock':
            sanitized_statement = """
            SELECT book.title, author.full_name as "author name", 
            stock.quantity, stock.leased, stock.quantity - stock.leased AS available
            FROM stock
            JOIN book ON stock.book_id = book.id
            JOIN author ON book.author_id = author.id"""
        # case ''
    return sanitized_statement


def tabulate_extracted_records(headers, records):
    """ Function to tabulate extracted database records """
    centered_headers = _center_align_headers(headers, records)
    return tabulate(records, headers=centered_headers, tablefmt='grid')


def terminate_program():
    """ Function to properly terminate program """
    sys.exit()
