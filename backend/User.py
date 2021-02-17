import sys

class User():
    __username  = ""
    __userID = None
    __lastname = ""
    __firstname = ""

    def __init__(self, username, id, firstname, lastname):
        self.__username = username
        self.__userID = id
        self.__firstname = firstname
        self.__lastname = lastname

    def get_name(self):
        return self.__lastname, self.__firstname

    def update_name(self, name_new, is_first):
        if is_first:
            self.__firstname = name_new
        else:
            self.__lastname = name_new

    def get_username(self):
        return self.__username

    def get_userID(self):
        return self.__userID