""" Module provides a decorator and functions for automatically adding generated special methods """
from dataclasses import dataclass

# Automatically generating common special methods, such as __init__, __repr__, and __eq__.


@dataclass
class Book:
    """ Class representing a book """
    author_id: int
    isbn: str
    title: str
    date_created: str

    # Setters, mutators

    def set_author_id(self, author_id):
        """ Function to set author id """
        self.author_id = author_id

    def set_isbn(self, isbn):
        """ Function to set isbn """
        self.isbn = isbn

    def set_title(self, title):
        """ Function to set title """
        self.title = title

    def set_date_created(self, date_created):
        """ Function to set date created """
        self.date_created = date_created

    # Getters, accessors

    def get_author_id(self):
        """ Function to return author id """
        return self.author_id

    def get_isbn(self):
        """ Function to return isbn """
        return self.isbn

    def get_title(self):
        """ Function to return title """
        return self.title

    def get_date_created(self):
        """ Function to return date created """
        return self.date_created
