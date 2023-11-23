""" Module provides a decorator and functions for automatically adding generated special methods """
from dataclasses import dataclass

# Automatically generating common special methods, such as __init__, __repr__, and __eq__.


@dataclass
class Author:
    """ Class representing an author """
    full_name: str
    country: str

    # Setters, mutators

    def set_full_name(self, full_name):
        """ Function to set full name """
        self.full_name = full_name

    def set_country(self, country):
        """ Function to set country """
        self.country = country

    # Getters, accessors

    def get_full_name(self):
        """ Function to return full name """
        return self.full_name

    def get_country(self):
        """ Function to return country """
        return self.country
