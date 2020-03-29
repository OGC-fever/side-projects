import geopandas as gp
import pandas as pd
import bs4, requests
import numpy as np
import io ,os
from bs4 import BeautifulSoup as bs
from zipfile import ZipFile
import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, 1)

url = 'https://www.water.gov.tw/opendata/qual5.csv'
hardness = pd.read_csv(url)
print(hardness.head())
# get city data and unpack zipfile
url_city = 'https://data.gov.tw/dataset/7441'
soup_city = bs(io.StringIO(requests.get(url_city).content.decode('utf-8')), 'html.parser')
link_city = soup_city.find('a', text = 'SHP').get('href')
with ZipFile(io.BytesIO(requests.get(link_city).content)) as file_city:
    for i in range(len(file_city.infolist())):
        print(file_city.infolist()[i])
    file_city.extractall()
# del unused files
del_files = []
shp_files = []
for i, j in enumerate(os.listdir()):
    if 'TOWN' not in j:
        if 'py' not in j:
            del_files.append(j)
    elif 'TOWN' in j:
        shp_files.append(j)
for i, j in enumerate(del_files):
    os.remove(del_files[i])

fig, ax = plt.subplots(1, 1)
map_data = gp.read_file(shp_files[-1])
map_data.plot(ax = ax, legend = True)
plt.show()
