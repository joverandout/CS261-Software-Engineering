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
    t1 = template("template1", ["happy", "sad"], ["is cereal a soup?"])
    m1 = t1.make_new_meetings("Title", "Category", "Code", datetime.now(), datetime.now(), h1, False)

    participants = [p1, p2]
    for p in participants:
        m1.update_participants(p)
    
    print(m1.to_string())
    return select_top_value(connect(db))

def select_top_value(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM HOSTS")

    rows = cur.fetchall()

    return rows

def connect(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    
    return conn