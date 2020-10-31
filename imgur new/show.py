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
img_columns = 3
url = link[0:img_columns]
page, soup, img_url, pic = [], [], [], []
for i in range(len(url)):
    page.append(requests.get(url[i]))
    soup.append(bs(page[i].content, 'lxml'))
    img_url.append(soup[i].find_all(
        'meta', {'name': "twitter:image"})[0]["content"])
    pic.append(np.array(Image.open(
        BytesIO(requests.get(img_url[i], stream=True, timeout=3).content))))
img_hight = 5
fig, ax = plt.subplots(1, len(url))
fig.set_tight_layout("tight")
fig.set_size_inches(img_hight * len(url), img_hight)
for i in range(len(url)):
    plt.imshow(pic[i])
    ax[i].set_axis_off()
    ax[i].imshow(pic[i])
plt.show()
