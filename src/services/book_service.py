" Class to manage books "
import itertools
import sqlite3
from src.classes import book
from src.services import author_service
from src.utils import utilities, common_database_operations

_database_path = utilities.get_database_path()


def get_book_info(infor):
    """ Function to extract book info and check if info is valid """
    info = ''
    while True:
        info = utilities.format_to_title_case(
            input(f"Enter book's {infor} {'(13 digits)' if infor == 'isbn' else ''}: "))
        if infor == 'isbn' and utilities.is_valid_isbn(info):
            break
        if not infor == 'isbn' and utilities.is_valid_str(info):
            break
    return info


def get_book_information():
    """ Function get book information """
    author_name = author_service.get_author_name()
    if author_service.is_author_exits(author_name):
        author_id = author_service.get_author_id(author_name)
        title = get_book_info('title')
        isbn = get_book_info('isbn')
        return book.Book(author_id, isbn, title, utilities.get_current_date())
    return False


# Search by book title or isbn??
def is_book_exits(book_title):
    """ Function to check if author already exists """
    obj_database_operations = common_database_operations.DatabaseOperations()
    if not obj_database_operations.is_table_empty('book'):
        return obj_database_operations.is_value_in_table('book', 'title', book_title)
    return False


def get_book_id(book_title):
    """ Function to get book id """
    obj_database_operations = common_database_operations.DatabaseOperations()
    if not obj_database_operations.is_table_empty('book'):
        return obj_database_operations.get_id('book', 'title', book_title)
    return -1


def add_book_to_database(book_information):
    """ Function insert new book """
    # int(id_num),
    book_info = (book_information.author_id, book_information.isbn,
                 book_information.title, book_information.date_created)
    try:
        with sqlite3.connect(_database_path) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO book (author_id, isbn, title, date_created) VALUES (?, ?, ?, ?)"
            cursor.execute(query, book_info)
            connection.commit()
        return cursor.lastrowid
    except sqlite3.DatabaseError as error:
        return utilities.database_operational_error(error=error)


def update_book(current_book_title, new_book_title):
    """ Function to update book title """
    if is_book_exits(current_book_title):
        book_id = get_book_id(current_book_title)
        obj_database_operations = common_database_operations.DatabaseOperations()
        obj_database_operations.update_record(
            'book', 'title', book_id, new_book_title)
        return True
    return False
    # return f"Sorry, but we don't have any book with title {current_book_title}. To update book, enter existing book."


def _get_stock_data(book_id):
    """ Function to check if book is leased """
    obj_database_operations = common_database_operations.DatabaseOperations()
    stock = obj_database_operations.fetch_record(
        'stock', 'book_id', book_id, False)
    return list(itertools.chain.from_iterable(stock))


def _check_book_leased(stock_data):
    """ Function to check if author has any leased book """
    for stock_item in stock_data:
        if stock_item[2] != stock_item[4]:
            return False
    return True

# ['The Divine Comedy' 0, 'Dante Alighieri' 1, 6 2, 0 3, 6 4]


def delete_book(book_title):
    """ Function to delete book """
    book_id = get_book_id(book_title)
    stock = _get_stock_data(book_id)
    obj_database_operations = common_database_operations.DatabaseOperations()
    if _check_book_leased(stock):
        obj_database_operations.delete_record('stock', book_id)
        obj_database_operations.delete_record('book', book_id)
        return True
    return False
