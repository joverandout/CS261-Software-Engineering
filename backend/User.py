import sys

class User():
    __username  = ""
    __userID = None

    def __init__(self, username, id):
        self.__username = username
        self.__userID = id


    def get_username(self):
        return self.__username

    def get_userID(self):
        return self.__userID