from datetime import datetime
import sys

class Meeting():
    title = ""
    category = ""
    code = ""
    __starttime = None
    __duration = None
    __host = None
    __participants = None
    __in_progress = None
    
    def __init__(self, title, category, code, startime, duration, host, in_progress):
        self.title = title
        self.category = category
        self.code = code
        self.__starttime = startime
        self.__duration = duration
        self.__host = host
        self.__participants = []
        self.__in_progress = in_progress

    def start_meeting(self):
        self.__in_progress = True
    
    #change the progress of the meeting to end it
    def end_meeting(self):
        self.__in_progress = False
    
    #return a boolean, true if a meeting has overrun and false otherwise
    def meeting_overrun(self):
        if datetime.now() - self.__starttime > self.__duration:
            return True
        return False

    #add a participant to the list of participants of a meeting
    def update_participants(self, participant):
        self.__participants.append(participant)

    #return the number of participants in a meeting as an integer
    def get_number_of_participants(self):
        return len(self.__participants)

    #change the host of the meeting to a new one since the host is a private
    #variable this needs to be a procedure
    def change_host(self, new_host):
        self.__host = new_host

    def to_string(self):
        string = "+++++++++++++++++++++\n"
        string += "| MEETING: "
        string += self.title
        string += "\n| Startime: "
        string += str(self.__starttime)
        string += "\n| host: \n|  -> ["
        string += self.__host.to_string()
        string += "]\n| " + str(self.get_number_of_participants()) + " participants:"
        for p in self.__participants:
            string += "\n|  -> ["
            string += p.to_string()
            string += "]"
        string += "\n| ongoing: "
        string += str(self.__in_progress)
        string += "\n+++++++++++++++++++++"
        return string

