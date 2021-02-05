from flask import Flask, url_for
from flask import request
from markupsafe import escape

import sqlite3
from sqlite3 import Error

import template_db_fethcer

app = Flask(__name__)

@app.route('/')
def index():
    return 'index'
    

@app.route('/login')
def login():
    return 'login'

@app.route('/user/<username>')
def profile(username):
    if username == 'Susan':
        return 'lol meme'
    if username == 'template':
        rows = template_db_fethcer.get_template_from_database('database.db')
        for row in rows:
            return(str(row))
    return '{}\'s profile'.format(escape(username))

with app.test_request_context():
    print(url_for('index'))
    print(url_for('login'))
    print(url_for('login', next='/'))
    print(url_for('profile', username='John Doe'))
    print(url_for('profile', username='Susan'))
    print(url_for('profile', username='template'))
