import sys
from Meeting import Meeting

class Template():
    name = ""
    __emotions = []
    __questions = []

    def __init__(self, name, __emotions, __questions):
        self.name = name
        self.__emotions = __emotions
        self.__questions = __questions

    def update_emotions(self, emotion, should_remove):
        if should_remove:
            __emotions.remove(emotion)
        else:
            __emotions.append(emotion)

    def get_emotions(self):
        return self.__emotions

    def get_questions(self):
        return self.__questions

    def update_question(self, question, should_remove):
        if should_remove:
            self.__questions.remove(should_remove)
        else:
            self.__questions.append(question)

    def make_new_meetings(self, title, category, code, startime, duration, host, in_progress):
        m1 = Meeting(self, title, category, code, startime, duration, host, in_progress, self)
        return m1
