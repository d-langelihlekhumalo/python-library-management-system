""" Testing the Library System """
import unittest
from src.services import author_service, book_service, stock_management
from src.classes import author, book, stock, checkout


class TestMain(unittest.TestCase):
    """ Class to test the Library System """

    # Function to check if author exists
    def test_check_existing_author(self):
        """ Test if author exists | Should return True """
        author_info = author.Author('William Shakespear', 'England')
        is_author_exists = author_service.is_author_exits(
            author_info.get_full_name())
        self.assertEqual(is_author_exists, False)

    # Function to update author information
    def test_update_author(self):
        """ Test to update author full name | Should return True """
        update_author = 'William Shakespeare'
        is_author_updated = author_service.update_author(
            update_author, 'William Shakespeare')
        self.assertEqual(is_author_updated, False)

    def test_delete_author(self):
        """ Test to delete an author | Should return false """
        author_name = 'Chinua Achebe'
        is_author_deleted = author_service.delete_author(author_name)
        self.assertEqual(is_author_deleted, False)

    # Function to check if book exists

    def test_check_existing_book(self):
        """ Test if book exists | Should return True """
        book_title = 'Romeo & Juliet'
        is_book_exists = book_service.is_book_exits(book_title)
        self.assertEqual(is_book_exists, True)

    # Function to update book information
    def test_update_book(self):
        """ Test to update book full name | Should return True """
        book_info = book.Book(39, '9780743477123',
                              'Hamlets', '22/08/2023')
        is_book_updated = book_service.update_book(
            book_info.get_title(), 'Hamlets')
        self.assertEqual(is_book_updated, False)

    def test_delete_book(self):
        """ Test to delete an book | Should return false """
        book_name = 'Things Fall Apart'
        is_book_deleted = book_service.delete_book(book_name)
        self.assertEqual(is_book_deleted, False)

    def test_checkout_book(self):
        """ Test to checkout a book | Should return true """
        book_title = 'Things Fall Apart'
        current_stock = stock.Stock(1, 8, 4)
        updated_stock = checkout.Checkout(1, 1)
        message = f"{updated_stock.quantity} copie(s) of {book_title} have been successfully leased"
        lease_book = stock_management.add_checkout_return(
            book_title, current_stock, updated_stock, 'lease')
        assert lease_book == message

    def test_attempt_to_checkout_book(self):
        """ Test checking out a book with invalid data | Should return false """
        book_title = 'JavaScript Design Patterns'
        current_stock = stock.Stock(67, 6, 0)
        updated_stock = checkout.Checkout(67, 7)
        message = f"Unable to lease {updated_stock.quantity} copies of {book_title}, we currently have {current_stock.quantity} copies available."
        lease_book = stock_management.add_checkout_return(
            book_title, current_stock, updated_stock, 'lease')
        assert lease_book == message

    def test_return_book(self):
        """ Test to return a book | Should return true """
        book_title = 'Things Fall Apart'
        current_stock = stock.Stock(1, 8, 4)
        updated_stock = checkout.Checkout(1, 1)
        message = f"{updated_stock.quantity} copie(s) of {book_title} have been successfully returned"
        lease_book = stock_management.add_checkout_return(
            book_title, current_stock, updated_stock, 'returned')
        assert lease_book == message


if __name__ == '__main__':
    unittest.main()
