from bs4 import BeautifulSoup as bs
import requests
from config import ptt_app
from flask import render_template, request
import math


@ptt_app.route("/list", methods=["GET"])
def hot_list():
    url = "https://www.ptt.cc/bbs/index.html"
    res = requests.get(url)
    html = bs(res.content, 'lxml')
    data = get_list(html)
    json = {}
    for index, item in enumerate(data):
        json[str(index+1).zfill(len(str(len(data))))] =\
            {"name": item[0], "title": item[1]}
    return json


def get_list(html):
    data = []
    board_name = html.find_all("div", {"class": "board-name"})
    board_title = html.find_all("div", {"class": "board-title"})
    while len(data) < 10:
        data.append([board_name[len(data)].text, board_title[len(data)].text])
    return data


def get_content(html):
    data = []
    for item in html.find_all("div", class_="r-ent"):
        data.append([item.a.text,
                     item.a["href"].split("/", 2)[-1],
                     item.find("div", {"class": "date"}).text,
                     item.find("div", {"class": "nrec"}).text,
                     item.find("div", {"class": "author"}).text])
    return data


@ptt_app.route("/", methods=["GET", "POST"])
def ptt_search():
    if request.method == "GET":
        return render_template("ptt/ptt.html", json=hot_list())
    board = request.form['board']
    keyword = request.form['keyword']
    author = request.form['author']
    count = request.form['count']
    query_prms = ""
    if not count:
        count = 10
    else:
        count = int(count)
    if not board:
        board = "allpost"
    if keyword and author:
        query_prms = f"{keyword}+author:{author}"
    if keyword and not author:
        query_prms = f"{keyword}"
    if not keyword and author:
        query_prms = f"author:{author}"
    if not keyword and not author:
        return render_template("ptt/ptt.html")
    url = "https://www.ptt.cc/bbs"
    search_url = f"{url}/{board}/search?q={query_prms}"
    cookies = {'over18': "1"}
    res = requests.get(search_url, cookies=cookies)
    html = bs(res.content, 'lxml')
    data = get_content(html)  # list
    if len(data) > count:
        data = data[:count]
    elif len(data) < count:
        page = math.ceil(count/20)
        for page in range(2, page + 1):
            back_url = f"{url}/{board}/search?page={page}&q={query_prms}"
            res = requests.get(back_url, cookies=cookies)
            html = bs(res.content, 'lxml')
            temp = get_content(html)
            data.extend(temp)
    temp = 0
    json = {}
    for item in data:
        if len(json.keys()) >= count:
            break
        temp += 1
        json[str(temp).zfill(len(str(count)))] =\
            {"title": item[0],
             "url": f"{url}/{item[1]}",
             "push": item[3],
             "author": item[4],
             "date": item[2].strip()}
    return render_template("ptt/ptt.html", data=json)
