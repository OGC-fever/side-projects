import sqlite3
from datetime import datetime
import random
import string
from random import randint


def init_db():
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.executescript('''
        create table if not exists calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            comments TEXT NOT NULL,
            time TEXT,
            rank INTEGER
        );''')
    con.commit()
    con.close()


def get_data():
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.execute('select * from comments')
    data = cur.fetchall()
    con.close()
    return f"{data[0:5]}"


database = 'spam_calls.db'
