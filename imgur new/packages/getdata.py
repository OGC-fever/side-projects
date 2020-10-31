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
output = soup.find_all("a",{"class":"image-list-link","data-page":"0"})
link_prefix = "https://imgur.com"
link = []
for i in range(len(output)):
    link.append(link_prefix + output[i]['href'])