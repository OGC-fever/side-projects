import pandas as pd
import bs4
import requests
import numpy as np

url = 'https://data.gov.tw/dataset/14200'
req = requests.get(url)
soup = bs4.BeautifulSoup(req.content, 'html.parser')
soup.find_all(class_ = 'dgresource')[0]