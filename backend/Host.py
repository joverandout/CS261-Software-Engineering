from datetime import datetime
import sys

class Host():
    __firstname = ""
    __lastname = ""
    __hashed_password = ""

def __init__(self, firstname, lastname, password):
    this.__firstname = firstname
    this.__lastname = lastname
    this.__hashed_password = password

def change_password(self, password_entered, new_password):
    if check_password(password_entered):
        this.__hashed_password = new_password
	return True
    return False

def get_name(self):
    return this.__firstname, this.__lastname

def update_name(self, name_new, is_first):
    if is_first:
        this.__firstname = name_new
    else:
	this.__lastname = name_new

def check_password(self, password_entered):
    if password_entered == self.__hasked_password:
	return True
    return False
