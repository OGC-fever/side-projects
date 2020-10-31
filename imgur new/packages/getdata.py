import random
from random import randint
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO

url = "https://imgur.com/hot/time"
page = requests.get(url)
soup = bs(page.content, "lxml")
output = soup.find_all("a", {"class": "image-list-link", "data-page": "0"})
link_prefix = "https://imgur.com"
link = []
for i in range(len(output)):
    link.append(link_prefix + output[i]['href'])
img_columns = 5
url = link[0:img_columns]
page, soup, img_url, pic = [], [], [], []
for i in range(len(url)):
    page.append(requests.get(url[i]))
    soup.append(bs(page[i].content, 'lxml'))
    img_url.append(soup[i].find_all(
        'meta', {'name': "twitter:image"})[0]["content"])
    pic.append(np.array(Image.open(BytesIO(requests.get(img_url[i]).content))))