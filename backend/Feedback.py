import sys

class Feedback():
    __emotions_selected = []
    __text_response = ""
    __attendee = None
    __is_technical = False

    def __init__(self, emotions, response, user, is_technical):
        self.__emotions_selected.append(emotions)
        self.__text_response = response
        self.__attendee = user
        self.__is_technical = is_technical

    def add_emotion(self, emotion):
        self.__emotions_selected.append(emotion)
    
    def get_emotions(self):
        return self.__emotions_selected
    
    def change_attendee(self, new_attendee):
        self.__attendee = new_attendee 
    
    def get_attendee(self):
        return self.__attendee
    
    def get_text_response(self):
        return self.__text_response
    
    def change_text_response(self, new_self):
        self.__text_response = new_self
    
    def get_is_technical(self):
        return self.__is_technical
    
    def change_is_technical(self):
        self.__is_technical = not self.__is_technical