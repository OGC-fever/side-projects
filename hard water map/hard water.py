import geopandas as gp
import pandas as pd
import bs4, requests, io, os
import numpy as np
from bs4 import BeautifulSoup as bs
from zipfile import ZipFile as zf
import matplotlib.pyplot as plt
# get hardness data
url = 'https://www.water.gov.tw/opendata/qual5.csv'
hardness = pd.read_csv(url)
# print(hardness.head())
# get city data and unpack zipfile
url_city = 'https://data.gov.tw/dataset/7441'
soup_city = bs(io.StringIO(requests.get(url_city).content.decode('utf-8')), 'html.parser')
link_city = soup_city.find('a', text = 'SHP').get('href')
with zf(io.BytesIO(requests.get(link_city, stream = True, timeout = 5).content)) as file_city:
    # for i, j in enumerate(file_city.infolist()):
        # print(file_city.infolist()[i])
    file_city.extractall()
# del unused files
del_files, shp_files = [], []
for i, j in enumerate(os.listdir()):
    if 'TOWN' not in j:
        if 'py' not in j:
            del_files.append(j)
    elif 'TOWN' in j:
        shp_files.append(j)
for i, j in enumerate(del_files):
    os.remove(del_files[i])
# read/filter city hardness and map, combine together
map_data = gp.read_file(shp_files[-1], encoding = 'utf-8')
city_data = hardness[hardness[hardness.columns[0]].str.contains('彰化')]
city_data.sort_values(by = city_data.columns[1], inplace = True)
city_data.reset_index(drop = 1, inplace = True)
city_map = map_data[map_data[map_data.columns[2]].str.contains('彰化')]
city_map.drop(city_map.columns[[0,1,4,5,6]], axis = 1, inplace = True)
city_map.sort_values(by = city_map.columns[1], inplace = True)
city_map.reset_index(drop = 1, inplace = True)
plot_data = city_map.join(city_data)
plot_data.drop(plot_data.columns[:2], axis = 1, inplace = True)
# set plot and show

fig, ax = plt.subplots(1, 1)

map_data.plot(ax = ax, legend = True)
plt.show()
