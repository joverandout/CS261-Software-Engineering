import template_db_fethcer
from Meeting import Meeting
from Host import Host
from datetime import datetime

import sqlite3
from sqlite3 import Error

def get_template_from_database(db):
    h1 = Host("user123", "9999", "John", "Smith", "password123")
    m1 = Meeting("Title", "Category", "Code", datetime.now(), datetime.now(), h1, False)
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