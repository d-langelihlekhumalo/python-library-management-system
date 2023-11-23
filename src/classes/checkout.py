""" Module provides a decorator and functions for automatically adding generated special methods """
from dataclasses import dataclass

# Automatically generating common special methods, such as __init__, __repr__, and __eq__.


@dataclass
class Checkout:
    """ Class representing checkout operation """
    book_id: int
    quantity: int

    def set_quantity(self, quantity):
        """ Function to set quantity """
        self.quantity = quantity

     # Getters, accessors

    def get_book_id(self):
        """ Function to return full name """
        return self.book_id

    def get_quantity(self):
        """ Function to return quantity """
        return self.quantity
