import template_db_fethcer
from Meeting import Meeting
from Host import Host
from Attendee import Attendee
from datetime import datetime
from Template import Template

import sqlite3
from sqlite3 import Error

def get_template_from_database(db):
    h1 = Host("user123", "9999", "John", "Smith", "password123")
    p1 = Attendee("attendee123", "1", "name", "name", True)
    p2 = Attendee("attendee124", "2", "Jackie", "Cooper", False)
    t1 = Template("template1", ["happy", "sad"], ["is cereal a soup?"])
    m1 = t1.make_new_meetings("Title", "Category", "Code", datetime.now(), datetime.now(), h1, False)

    participants = [p1, p2]
    for p in participants:
        m1.update_participants(p)
    
    print(m1.to_string())
    return select_top_value(connect(db), h1)

def select_top_value(conn, h1):
    cur = conn.cursor()
    input = 1
    cur.execute("SELECT TemplateName, EmotionsSelected, Question, TemplateID FROM TEMPLATES WHERE TemplateID = " + str(input))

    rows = cur.fetchall()
    row = rows[0]

    emotions = row[1].split (",")
    questions = row[2].split(",")
    templateID = row[3]

    t2 = Template(row[0], emotions, questions)

    cur.execute("SELECT MeetingName, Category, Starttime FROM MEETING WHERE TemplateID =" + str(templateID))

    rows = cur.fetchall()

    row = rows[0]

    m2 = t2.make_new_meetings(row[0], row[1], "CODE", row[2], datetime.now(), h1, False)
    return m2.to_string()


def connect(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    
    return conn
