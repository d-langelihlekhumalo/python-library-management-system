""" Main Program """
from src.classes import author, book  # , stock, checkout
# author_service, book_service, stock_service, checkout_service
from src.services import menu_service, author_service, book_service, stock_service, stock_management
from src.utils import utilities
from src.utils import common_database_operations

obj_database_operations = common_database_operations.DatabaseOperations()


def from_database_display(table_name):
    """ Function to display specified table """
    if obj_database_operations.is_table_exists(table_name):
        if not obj_database_operations.is_table_empty(table_name):
            return obj_database_operations.fetch_all_records(table_name, True)
        return f"Table {table_name}'s has no data to display"
    return "Unexpected Error, please try again later."


def insert_menu_handler():
    """ Function to handle and route insert menu requests """
    print(menu_service.insert_menu())
    return_to_main_menu = False
    while True:
        users_choice = input("Enter insert menu choice[1 - 3]: ")
        if utilities.is_single_digit(users_choice):
            if utilities.is_valid_option(users_choice, 1, 3):
                match int(users_choice):
                    case 1:
                        author_name = author_service.get_author_name()
                        if author_service.is_author_exits(author_name):
                            print(
                                f"Author: {utilities.format_to_title_case(author_name)}, already exists.")
                        else:
                            country = author_service.get_author_origin()
                            author_info = author.Author(utilities.format_to_title_case(
                                author_name), utilities.format_to_title_case(country))
                            # total_rows = obj_database_operations.num_total_rows(
                            #     'author') + 1
                            # total_rows,
                            last_row_id = author_service.add_author(
                                author_info)
                            if isinstance(last_row_id, int):
                                print(
                                    f"Author: {utilities.format_to_title_case(author_name)}, has been successfully added with id: {last_row_id}")
                            else:
                                print(
                                    f"Sorry, but we couldn't add author: {utilities.format_to_title_case(author_name)}\nLast Row: {last_row_id}")
                    case 2:
                        book_info = book_service.get_book_information()
                        # Check if author was found
                        if not book_info is False:
                            qauntity = stock_service.get_stock_quantity(
                                book_info.title)
                            if not isinstance(book_info, book.Book):
                                print(
                                    "Author not found. Ensure that author's name has been entered correctly and that the author exists.")
                            else:
                                extracted_book = obj_database_operations.fetch_record(
                                    'book', 'title', book_info.title, False)

                                if not book_service.is_book_exits(book_info.title) and not extracted_book[0] == book_info.isbn:
                                    if not obj_database_operations.is_value_in_table('book', 'isbn', book_info.isbn):
                                        # total_rows = obj_database_operations.num_total_rows(
                                        #     'book') + 1
                                        # total_rows,
                                        last_row_id = book_service.add_book_to_database(
                                            book_info)
                                        if isinstance(last_row_id, int):
                                            book_id = book_service.get_book_id(
                                                book_info.get_title())
                                            stock_info = stock_service.get_stock_default_info(
                                                book_id, qauntity)
                                            # stock_id = obj_database_operations.num_total_rows(
                                            #     'stock') + 1
                                            # stock_id,
                                            stock_service.add_stock_to_database(
                                                stock_info)
                                            print(
                                                f"Book: {utilities.format_to_title_case(book_info.title)}, has been successfully added with id: {last_row_id}")
                                        else:
                                            print(
                                                f"Sorry, but we couldn't add book: {utilities.format_to_title_case(book_info.title)}\nLast Row: {last_row_id}")
                                    else:
                                        print(
                                            f"Book isbn: {book_info.isbn} alread exists, please enter unique isbn for book: {book_info.title}")
                                else:
                                    print(
                                        f"Book with title {book_info.title} and isbn {book_info.isbn} already exists. Please increase quantity istead.")
                        else:
                            print(
                                "Author not found. Ensure that author's name has been entered correctly and that the author exists.")
                    case 3:
                        return_to_main_menu = True
                if return_to_main_menu:
                    main_menu_handler()


def display_menu_handler():
    """ Function to handle and route display menu requests """
    print(menu_service.display_menu())
    return_to_main_menu = False
    while True:
        users_choice = input("Enter display menu choice[1 - 3]: ")
        if utilities.is_single_digit(users_choice):
            if utilities.is_valid_option(users_choice, 1, 3):
                match int(users_choice):
                    case 1:
                        print(from_database_display('author'))
                    case 2:
                        print(from_database_display('book'))
                    case 3:
                        return_to_main_menu = True
                if return_to_main_menu:
                    main_menu_handler()
                print(menu_service.display_menu())


def update_menu_handler():
    """ Function to handle and route update menu requests """
    print(menu_service.update_menu())
    return_to_main_menu = False
    while True:
        users_choice = input("Enter update menu choice[1 - 3]: ")
        if utilities.is_single_digit(users_choice):
            if utilities.is_valid_option(users_choice, 1, 3):
                match int(users_choice):
                    case 1:
                        author_name = author_service.get_author_name(
                            ' current')
                        updated_author_name = author_service.get_author_name(
                            ' new')
                        is_author_updated = author_service.update_author(
                            author_name, updated_author_name)
                        if is_author_updated:
                            print(
                                f"Author: {author_name} has been updated to {updated_author_name}")
                        else:
                            print(
                                f"Sorry, but we don't have any author with name {author_name}. To update author, enter existing author.")
                            # print(is_author_updated)
                    case 2:
                        book_title = book_service.get_book_info(
                            'current title')
                        updated_book_title = book_service.get_book_info(
                            'new title')
                        is_book_updated = book_service.update_book(
                            book_title, updated_book_title)
                        if is_book_updated:
                            print(
                                f"Book: {book_title} has been updated to {updated_book_title}")
                        else:
                            print(
                                f"Sorry, but we don't have any book with title {book_title}. To update book, enter existing book.")
                            # print(is_book_updated)
                    case 3:
                        return_to_main_menu = True
                if return_to_main_menu:
                    main_menu_handler()


def delete_menu_handler():
    """ Function to handle and route delete menu requests """
    print(menu_service.delete_menu())
    return_to_main_menu = False
    while True:
        users_choice = input("Enter delete menu choice[1 - 3]: ")
        if utilities.is_single_digit(users_choice):
            if utilities.is_valid_option(users_choice, 1, 3):
                match int(users_choice):
                    case 1:
                        author_name = author_service.get_author_name()
                        if author_service.is_author_exits(author_name):
                            if author_service.delete_author(author_name):
                                print(
                                    f"Author: {utilities.format_to_title_case(author_name)} has been successuflly deleted.")
                            else:
                                print(
                                    f"Author: {utilities.format_to_title_case(author_name)} can't be deleted, has some book(s) leased out.")
                        else:
                            print(
                                f"We don't have an author with name: {utilities.format_to_title_case(author_name)}")
                    case 2:
                        book_title = book_service.get_book_info('title')
                        if book_service.is_book_exits(book_title):
                            book_service.delete_book(book_title)
                            if book_service.delete_book(book_title):
                                print(
                                    f"Book: {utilities.format_to_title_case(book_title)} has been successuflly deleted.")
                            else:
                                print(
                                    f"Book: {utilities.format_to_title_case(book_title)} can't be deleted, some copies are leased out.")
                        else:
                            print(
                                f"We don't have a book with title: {utilities.format_to_title_case(book_title)}")
                    case 3:
                        return_to_main_menu = True
                if return_to_main_menu:
                    main_menu_handler()


def search_menu_handler():
    """ Function to handle and route search menu requests """
    print(menu_service.search_menu())
    return_to_main_menu = False
    while True:
        users_choice = input("Enter search menu choice[1 - 4]: ")
        if utilities.is_single_digit(users_choice):
            if utilities.is_valid_option(users_choice, 1, 4):
                match int(users_choice):
                    case 1:
                        author_name = author_service.get_author_name()
                        if author_service.is_author_exits(author_name):
                            print(obj_database_operations.fetch_record('author', 'full_name',
                                                                       author_name, True))
                        else:
                            print(
                                f"We don't have any books authored by: {utilities.format_to_title_case(author_name)}")
                    case 2:
                        author_name = author_service.get_author_name()
                        if author_service.is_author_exits(author_name):
                            print(obj_database_operations.fetch_books_by_author(
                                author_name, True))
                        else:
                            print(
                                f"We don't have any books authored by: {utilities.format_to_title_case(author_name)}")
                    case 3:
                        book_title = book_service.get_book_info('title')
                        if book_service.is_book_exits(book_title):
                            print(obj_database_operations.fetch_record('book', 'title',
                                                                       book_title, True))
                        else:
                            print(
                                f"We don't have a book with title: {utilities.format_to_title_case(book_title)}")
                    case 4:
                        return_to_main_menu = True
                if return_to_main_menu:
                    main_menu_handler()


def manage_checkout_return(transaction_type):
    """ Function to manage checkout and return """
    book_title = book_service.get_book_info('title')
    if book_service.is_book_exits(book_title):
        book_id = book_service.get_book_id(book_title)
        quantity = 0
        if transaction_type == 'lease':
            quantity = stock_service.get_stock_quantity(
                book_name=book_title, is_checkout=True)
        else:
            quantity = stock_service.get_stock_quantity(
                book_name=book_title, is_checkout=False, is_return=True)
        current_stock = stock_management.get_current_stock(
            book_id, book_title)
        lease_information = stock_management.get_stock_checkout_information(
            book_id, quantity)
        return stock_management.add_checkout_return(
            book_title, current_stock, lease_information, transaction_type)
    return f"We don't have a book with title: {utilities.format_to_title_case(book_title)}"


def main_menu_handler():
    """ Function to handle and route main menu requests """
    print(menu_service.main_menu())
    return_to_main_menu = False
    while True:
        users_choice = input("Enter main menu choice[1 - 8]: ")
        if utilities.is_single_digit(users_choice):
            if utilities.is_valid_option(users_choice, 1, 8):
                match int(users_choice):
                    case 1:
                        insert_menu_handler()
                    case 2:
                        display_menu_handler()
                    case 3:
                        update_menu_handler()
                    case 4:
                        delete_menu_handler()
                    case 5:
                        search_menu_handler()
                    case 6:
                        print(manage_checkout_return('lease'))
                    case 7:
                        print(manage_checkout_return('return'))
                    case 8:
                        utilities.terminate_program()
                if return_to_main_menu:
                    main_menu_handler()


main_menu_handler()
