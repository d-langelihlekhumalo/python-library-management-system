""" Class to manage and maintaince an stock """
# import sqlite3
from src.classes import stock, checkout
from src.utils import utilities, common_database_operations

_database_path = utilities.get_database_path()


def get_stock_checkout_information(book_id, quantity):
    """ Function get checkout information """
    return checkout.Checkout(int(book_id), int(quantity))


def get_checkout_id(book_id):
    """ Function to get stock id """
    obj_database_operations = common_database_operations.DatabaseOperations()
    if not obj_database_operations.is_table_empty('stock'):
        return obj_database_operations.get_id('stock', 'book_id', book_id)
    return -1


def get_current_stock(book_id, book_title):
    """ Function to get current stock info """
    obj_database_operations = common_database_operations.DatabaseOperations()
    if not obj_database_operations.is_table_empty('stock'):
        if obj_database_operations.is_value_in_table('stock', 'book_id', book_id):
            current_stock = obj_database_operations.fetch_record(
                'stock', 'book_id', book_id, False)
            return stock.Stock(book_id, current_stock[0][2], current_stock[0][3])

    return f"Sorry, we can't lease book {book_title}, Please ensure it's been added in stock."


def add_checkout_return(book_title, current_stock, updated_stock, transaction_type):
    """ Function to add new checkout to database if vaild """
    message = f"Unable to {transaction_type} {updated_stock.quantity} copies of {book_title}"

    if int(updated_stock.quantity) > 0:
        # Handle leasing of books
        if transaction_type == 'lease':
            available_quantity = int(
                current_stock.quantity) - int(current_stock.leased)
            if int(available_quantity) >= int(updated_stock.quantity):
                total_leased_quantity = int(
                    current_stock.leased) + int(updated_stock.quantity)
                # print(
                # f"Current Leases: {current_stock.quantity} | Leasing {updated_stock.quantity} | Total: {total_leased_quantity}")
                return _update_checkout_return(book_title, current_stock.book_id, total_leased_quantity, 'leased', updated_stock.quantity)
            return f"{message}, we currently have {available_quantity} copies available."
        # Handle return of books
        total_return_quantity = int(
            current_stock.leased) - int(updated_stock.quantity)
        if int(current_stock.quantity) >= int(total_return_quantity) and int(current_stock.leased) > 0:
            return _update_checkout_return(book_title, current_stock.book_id, total_return_quantity, 'returned', updated_stock.quantity)
        return f"{message}. We only leased out {current_stock.leased} copies"

    return message


def _update_checkout_return(book_title, book_id, amount_leased_returned,
                            transaction_type, initial_return_amount=0):
    """ Update stock information """
    _update_checkout_return_ = common_database_operations.DatabaseOperations(
    ).update_record('stock', 'leased', book_id, amount_leased_returned)
    if isinstance(_update_checkout_return_, bool):
        # amount_leased_returned if transaction_type == 'leased' else
        return f"{initial_return_amount} copie(s) of {book_title} have been successfully {transaction_type}"
    return f"{_update_checkout_return_}"
