import template_db_fethcer

import sqlite3
from sqlite3 import Error

def get_template_from_database(db):
    return select_top_value(connect(db))

def select_top_value(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM TEMPLATES")

    rows = cur.fetchall()

    return rows

def connect(db):
    conn = None
    try:
        conn = sqlite3.connect(db)
    except Error as e:
        print(e)
    
    return conn