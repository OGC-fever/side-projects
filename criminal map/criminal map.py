import pandas as pd
import bs4
import requests
import numpy as np

url = 'https://data.gov.tw/dataset/14200'
req = requests.get(url)
soup = bs4.BeautifulSoup(req.content, 'html.parser')

titles = soup.find_all('span', class_ = 'ff-desc')

links = soup.find_all('a', class_ = 'dgresource', title="下載格式為 API")

for i in range(0,len(titles),2):
    print(titles[i].text)

for i in range(len(links)):
    print(links[i].text)
