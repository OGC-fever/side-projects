from re import T
from bs4 import BeautifulSoup as bs
import requests
from config import ptt_app
from flask import render_template, request, redirect, url_for


def get_back_url(url, page):
    back_url = ""
    for item in page.find_all(class_="btn wide"):
        if "上頁" in (item.text):
            back_url = url + "/" + item["href"].split("/")[-1]
    return back_url


def get_content(page):
    data = []
    for item in page.find_all("div", class_="r-ent"):
        try:
            data.append([item.a.text,
                         item.a["href"].split("/")[-1],
                         item.find(class_="date").text,
                         item.find(class_="author").text])
        except:
            pass
    return data


def pure_data(data, keyword):
    pure_data = []
    for item in data:
        if keyword.lower() in item[0].lower():
            pure_data.append(item)
    return pure_data


@ptt_app.route("/", methods=["POST"])
def ptt_search():
    board = request.form['board']
    keyword = request.form['keyword']
    author = request.form['author']
    count = request.form['count']
    query_prms = ""
    if not board:
        board = "allpost"
        if not keyword or not author:
            return render_template("ptt/ptt.html")
    if keyword and author:
        query_prms = f"{keyword}+author:{author}"
    if keyword and not author:
        query_prms = keyword
    if not keyword and author:
        query_prms = f"author:{author}"
    url = f"https://www.ptt.cc/bbs/{board}/search?q={query_prms}"
    cookies = {'over18': "1"}
    res = requests.get(url, cookies=cookies)
    page = bs(res.content, 'lxml')
    return str(page)
    data = get_content(page)  # list
    data.reverse()
    data = pure_data(data, keyword)
    while len(data) < count:
        back_url = get_back_url(url, page)
        res = requests.get(back_url, cookies=cookies)
        page = bs(res.content, 'lxml')
        temp = get_content(page)
        temp.reverse()
        data += temp
        data = pure_data(data, keyword)

# @ptt_app.route("/<board>/<keyword>/<int:count>", methods=["GET", "POST"])
# def ptt(board, keyword, count):
#     url = 'https://ptt.cc/bbs/' + board
#     cookies = {'over18': "1"}
#     res = requests.get(url, cookies=cookies)
#     page = bs(res.content, 'lxml')
#     data = get_content(page)  # list
#     data.reverse()
#     data = pure_data(data, keyword)
#     while len(data) < count:
#         back_url = get_back_url(url, page)
#         res = requests.get(back_url, cookies=cookies)
#         page = bs(res.content, 'lxml')
#         temp = get_content(page)
#         temp.reverse()
#         data += temp
#         data = pure_data(data, keyword)
#     temp = 0
#     json = {}
#     for item in data:
#         if len(json.keys()) >= count:
#             break
#         try:
#             if keyword.lower() in item[0].lower():
#                 temp += 1
#                 json[str(temp).zfill(len(str(count)))] =\
#                     {"title": item[0],
#                      "url": url+"/"+item[1],
#                      "date": item[2].strip(),
#                      "author": item[3]}
#         except TypeError:
#             pass

#     return render_template("ptt/ptt.html", data=json)
