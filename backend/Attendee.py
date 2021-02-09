from datetime import datetime
from User import User
import sys

class Attendee(User):
    __firstname = ""
    __lastname = ""
    __anonymous = False

    def __init__(self, username, user_id, firstname, lastname, anonymous):
        super().__init__(username, user_id, firstname, lastname)
        self.__anonymous = anonymous

    def get_attendee_name(self):
        if not self.__anonymous:
            return super().get_name()
        else:
            return "ANONYMOUS"

    def to_string(self):
        string = "username: "
        string += super().get_username()
        string += " | ID: "
        string += super().get_userID()
        string += " | Name : "
        string += str(self.get_attendee_name())
        string += ""
        return string

