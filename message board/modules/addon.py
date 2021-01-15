import sqlite3
from io import BytesIO
from PIL import Image
from random import randint


def verify():
    verify_len = 6
    text = ""
    for i in range(verify_len):
        text += str(randint(0, 9))
    return text


def init_db(database):
    sql = {
        "init_msg": "create table if not exists msg (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT NOT NULL,msg TEXT NOT NULL,time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,image blob,thumbnail blob)"}
    db_crud(database=database, sql=sql["init_msg"],
            prm="", fetch=False, commit=True, query=False)


def db_crud(database, sql, prm, fetch, commit, query):
    with sqlite3.connect(database) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        if prm == "":
            cur.execute(sql)
        if prm != "":
            cur.execute(sql, prm)
        if fetch != False:
            if fetch == "all":
                return cur.fetchall()
            if fetch == "one":
                return cur.fetchone()
        if commit:
            con.commit()
        if query:
            return cur.fetchone()[0]


def check_file(filename):
    file_exts = {'jpg', 'jpeg', "jfif", "png", "gif"}
    if filename and "." in filename:
        if filename.split(".")[-1].lower() in file_exts:
            return True
    else:
        return False


def get_file_ext(filename):
    ext = filename.split(".")[-1].upper()
    if ext == "JPG":
        ext = "JPEG"
    return ext


def make_timg(file, type):  # make thumbnail
    image_size = [(1000, 1000), (300, 300)]
    buf = BytesIO()
    im = Image.open(file)
    if type == "image":
        im.thumbnail(image_size[0])
    if type == "timg":
        im.thumbnail(image_size[1])
    im.save(buf, get_file_ext(file.filename))
    return buf
