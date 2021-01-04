import sqlite3

sql = {"init_msg": "create table if not exists msgs (\
                id INTEGER PRIMARY KEY AUTOINCREMENT,\
                name TEXT NOT NULL,\
                msg TEXT NOT NULL,\
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"}


def init_db(database):
    with sqlite3.connect(database) as con:
        cur = con.cursor()
        cur.execute(sql["init_msg"])
        con.commit()
