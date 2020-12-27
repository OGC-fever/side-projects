import sqlite3


def init_db():
    con = sqlite3.connect(database)
    cur = con.cursor()
    cur.executescript('''
        create table if not exists calls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT NOT NULL,
            comments TEXT NOT NULL,
            time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            rank INTEGER DEFAULT 0
        );''')
    con.commit()
    con.close()


database = 'spam_calls.db'
