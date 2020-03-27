import pandas as pd
import bs4
import requests
import numpy as np

url = 'https://data.gov.tw/dataset/14200'
req = requests.get(url)
soup = bs4.BeautifulSoup(req.content, 'html.parser')

soup1 = soup.find_all(class_ = 'dgresource', title="下載格式為 CSV")
soup2 = soup.find_all(class_ = 'ff-desc')

for i in range(len(soup2)):
    print(soup2[i].text)

for i in range(len(soup1)):
    print(soup1[i].text)


