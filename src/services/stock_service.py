" Class to manage books "
import sqlite3
from src.classes import stock
from src.utils import utilities

_database_path = utilities.get_database_path()


def get_stock_quantity(book_name, is_checkout=False, is_return=False):
    """ Function to return stock quantity """
    quantity = 0
    prompt = ''
    if is_return:
        prompt = "return"
    else:
        prompt = "add" if not is_checkout else "lease"
    while True:
        quantity = input(
            f"How many {book_name} books would you like to {prompt}: ")
        if quantity.isdigit():
            break
    return quantity


def get_stock_default_info(book_id, quantity):
    """ Function to return deafult stock """
    return stock.Stock(book_id, quantity, 0)


def add_stock_to_database(stock_information):
    """ Function insert new stock """
    # int(id_num),
    stock_info = (stock_information.book_id,
                  stock_information.quantity, stock_information.leased)
    try:
        with sqlite3.connect(_database_path) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO stock (book_id, quantity, leased) VALUES (?, ?, ?)"
            cursor.execute(query, stock_info)
            connection.commit()
        return cursor.lastrowid
    except sqlite3.DatabaseError as error:
        return utilities.database_operational_error(error=error)
