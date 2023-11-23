""" Class to manage and maintaince an author """
import itertools
import sqlite3
from src.classes import author
from src.utils import utilities, common_database_operations
_database_path = utilities.get_database_path()


def get_author_name(status=None):
    """ Function to get author name """

    full_name = utilities.get_full_name(
        f"author{status if not status is None else 's'}")
    return full_name


def get_author_origin():
    """ Function to get author origin """
    country = ''
    while True:
        country = input("Enter author's country: ")
        # Check if country is valid str
        if utilities.is_valid_str(country):
            break

        # If country empty return 'unknown'
        if str(country) == '' or str(country) == ' ':
            country = 'Unknown'
            break

    return country


def get_author_information():
    """ Function get author information """
    full_name = get_author_name()
    country = get_author_origin()
    return author.Author(full_name, country)


def is_author_exits(author_name):
    """ Function to check if author already exists """
    obj_database_operations = common_database_operations.DatabaseOperations()
    if not obj_database_operations.is_table_empty('author'):
        return obj_database_operations.is_value_in_table('author', 'full_name', author_name)
    return False


def get_author_id(author_name):
    """ Function to get author id """
    obj_database_operations = common_database_operations.DatabaseOperations()
    if not obj_database_operations.is_table_empty('author'):
        return obj_database_operations.get_id('author', 'full_name', author_name)
    return -1


def add_author(author_information):
    """ Function to add new author to database """
    obj_database_operations = common_database_operations.DatabaseOperations()
    if not obj_database_operations.is_table_empty('author'):
        if not obj_database_operations.is_value_in_table('author', 'full_name', author_information.full_name):
            return add_author_to_database(author_information)
    return False


def add_author_to_database(author_information):
    """ Function insert new author """
    author_info = (author_information.full_name,
                   author_information.country)
    # print(author_info)
    try:
        with sqlite3.connect(_database_path) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO author (full_name, country) VALUES (?, ?)"
            cursor.execute(query, author_info)
            connection.commit()
        return cursor.lastrowid
    except sqlite3.DatabaseError as error:
        return utilities.database_operational_error(error=error)


def update_author(current_author_full_name, new_author_full_name):
    """ Function to update author full_name """
    if is_author_exits(current_author_full_name):
        author_id = get_author_id(current_author_full_name)
        obj_database_operations = common_database_operations.DatabaseOperations()
        obj_database_operations.update_record(
            'author', 'full_name', author_id, new_author_full_name)
        return True
    return False

# f"Sorry, but we don't have any author with name {current_author_full_name}.
# To update author, enter existing author."


def _get_book_ids(author_name):
    """ Function to return book titles """
    books_by_author = common_database_operations.DatabaseOperations(
    ).fetch_books_by_author(author_name, False)

    if isinstance(books_by_author, list):
        book_titles = []
        # Extract book titles
        for item in books_by_author:
            title = item[0]
            book_titles.append(title)

        # Extract Ids
        book_ids = []
        for title in book_titles:
            book_ids.append(
                common_database_operations.DatabaseOperations().get_id('book', 'title', title))
        return _get_stock_data(book_ids)

    if 'currently has no books' in books_by_author:
        return books_by_author

    return False


def _get_stock_data(book_ids):
    """ Function to return book ids """
    stock_data = []
    for id_num in book_ids:
        stock_data.append(common_database_operations.DatabaseOperations(
        ).fetch_record('stock', 'book_id', id_num, False))

    return list(itertools.chain.from_iterable(stock_data))


def _check_book_leased(stock_data):
    """ Function to check if author has any leased book """
    for stock_item in stock_data:
        if stock_item[2] != stock_item[4]:
            return False
    return True


def delete_author(author_name):
    """ Function to delete author """
    stock_data = _get_book_ids(author_name)
    if not isinstance(stock_data, str) and stock_data:
        if _check_book_leased(stock_data):
            author_id = get_author_id(stock_data[0][1])
            counter = 0
            while counter < len(stock_data):
                book_id = common_database_operations.DatabaseOperations().get_id('book',
                                                                                 'author_id', author_id)
                common_database_operations.DatabaseOperations().delete_record('stock', book_id)
                common_database_operations.DatabaseOperations().delete_record('book', book_id)
                counter += 1
            common_database_operations.DatabaseOperations().delete_record('author', author_id)
            return True

    if isinstance(stock_data, str):
        author_id = get_author_id(author_name)
        common_database_operations.DatabaseOperations().delete_record('author', author_id)
        return True

    return False


# def delete_author(book_id, author_id):
#     """ Function to delete author """
#
