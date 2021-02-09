from datetime import datetime
from User import User
import sys

class Host(User):
    __firstname = ""
    __lastname = ""
    __hashed_password = ""

    def __init__(self, username, user_id, firstname, lastname, password):
        super().__init__(username, user_id)
        self.__firstname = firstname
        self.__lastname = lastname
        self.__hashed_password = password

    def change_password(self, password_entered, new_password):
        if self.check_password(password_entered):
            self.__hashed_password = new_password
            return True
        return False

    def get_name(self):
        return self.__firstname, self.__lastname

    def update_name(self, name_new, is_first):
        if is_first:
            self.__firstname = name_new
        else:
            self.__lastname = name_new

    def check_password(self, password_entered):
        if password_entered == self.__hashed_password:
            return True
        return False
        
    def to_string(self):
        string = "-> username: "
        string += super().get_username()
        string += " | ID: "
        string += super().get_userID()
        string += " | Name : "
        string += str(self.__lastname) + ", " + str(self.__firstname)
        string += " |"
        return string

