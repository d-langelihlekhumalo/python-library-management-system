# """ Class to manage and maintaince an author """
# import sqlite3
# from src.classes import checkout
# from src.utils import utilities, common_database_operations

# _database_path = utilities.get_database_path()


# def get_checkout_information(book_id, quantity):
#     """ Function get checkout information """
#     return checkout.Checkout(book_id, int(quantity), 'leased', utilities.get_current_date(), '')


# def get_checkout_id(book_id):
#     """ Function to get checkout id """
#     obj_database_operations = common_database_operations.DatabaseOperations()
#     if not obj_database_operations.is_table_empty('checkout'):
#         return obj_database_operations.get_id('checkout', 'book_id', book_id)
#     return -1


# def add_checkout(checout_num, checkout_information, book_infomation):
#     """ Function to add new checkout to database if vaild """
#     if not checkout_information.quantity <= 0:
#         return add_checkout_to_database(checout_num, checkout_information)
#     return f"Unable to lease {checkout_information.quantity} copies of {book_infomation.title}"


# def add_checkout_to_database(id_num, checkout_information):
#     """ Function insert new checkout """
#     checkout_info = (int(id_num), checkout_information.book_id,
#                      checkout_information.quantity, checkout_information.status, checkout_information.checkout_date, checkout_information.return_date)
#     return checkout_info
# try:
#     with sqlite3.connect(_database_path) as connection:
#         cursor = connection.cursor()
#         query = "INSERT INTO checkout (id, full_name, country) VALUES (?, ?, ?)"
#         cursor.execute(query, checkout_info)
#         connection.commit()
#     return cursor.lastrowid
# except sqlite3.DatabaseError as error:
#     return utilities.database_operational_error(error=error)


# def update_checkout(current_author_full_name, new_author_full_name):
#     """ Function to update author full_name """
#     if is_author_exits(current_author_full_name):
#         author_id = get_author_id(current_author_full_name)
#         obj_database_operations = common_database_operations.DatabaseOperations()
#         obj_database_operations.update_record(
#             'author', 'full_name', author_id, new_author_full_name)
#         return True
#     return f"Sorry, but we don't have any author with name {current_author_full_name}. To update author, enter existing author."
