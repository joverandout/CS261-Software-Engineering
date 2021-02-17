from datetime import datetime
from User import User
import sys

class Host(User):
    __firstname = ""
    __lastname = ""
    __hashed_password = ""

    def __init__(self, username, user_id, firstname, lastname, password):
        super().__init__(username, user_id, firstname, lastname)
        self.__hashed_password = password

    def change_password(self, password_entered, new_password):
        if self.check_password(password_entered):
            self.__hashed_password = new_password
            return True
        return False

    def check_password(self, password_entered):
        if password_entered == self.__hashed_password:
            return True
        return False
        
    def to_string(self):
        string = "username: "
        string += super().get_username()
        string += " | ID: "
        string += super().get_userID()
        string += " | Name : "
        string += str(super().get_name())
        string += ""
        return string

