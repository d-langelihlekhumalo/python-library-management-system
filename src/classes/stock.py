""" Module provides a decorator and functions for automatically adding generated special methods """
from dataclasses import dataclass

# Automatically generating common special methods, such as __init__, __repr__, and __eq__.


@dataclass
class Stock:
    """ Class representing a stock """
    book_id: int
    quantity: int
    leased: int

    # Setters, mutators

    def set_book_id(self, book_id):
        """ Function to set full name """
        self.book_id = book_id

    def set_quantity(self, quantity):
        """ Function to set quantity """
        self.quantity = quantity

    def set_leased(self, leased):
        """ Function to set leased """
        self.leased = leased

    # Getters, accessors

    def get_book_id(self):
        """ Function to return full name """
        return self.book_id

    def get_quantity(self):
        """ Function to return quantity """
        return self.quantity

    def get_leased(self):
        """ Function to return leased """
        return self.leased
