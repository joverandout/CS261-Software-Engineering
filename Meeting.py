from datetime import datetime
import sys

class Meeting():
    title = ""
    category = ""
    code = ""
    __starttime = None
    __duration = None
    __host = None
    __participatns = None
    __in_progress = None
    
    def __init__(self, title, category, code, startime, duration, host, in_progress):
        self.title = title
        self.category = category
        self.code = code
        self.__starttime = startime
        self.__duration = duration
        self.__host = host
        self.__participatns = []
        self.__in_progress = in_progress

    def start_meeting(self):
        self.__in_progress = True
    
    def end_meeting(self):
        self.__in_progress = False
    
    def meeting_overrun(self):
        if datetime.now() - self.__starttime > self.__duration:
            return True
        return False

    def to_string(self):
        string = ""
        string += "| MEETING: "
        string += self.title
        string += "\n| Startime: "
        string += str(self.__starttime)
        string += "\n| host: "
        string += self.__host
        string += "\n| ongoing: "
        string += str(self.__in_progress)
        return string

