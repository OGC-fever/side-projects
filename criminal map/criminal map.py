import geopandas as gp
import pandas as pd
import bs4, requests, io, os
import numpy as np
from bs4 import BeautifulSoup as bs
from zipfile import ZipFile as zf
import matplotlib.pyplot as plt
# get criminal data and unpack zipfile
url_criminal = 'https://data.gov.tw/dataset/14200'
timeout = 3
soup_criminal = bs(io.StringIO(requests.get(url_criminal, stream = True, timeout = timeout).content.decode('utf-8')), 'html.parser')
titles_criminal = soup_criminal.find_all('span', class_ = 'ff-desc')
links_criminal = soup_criminal.find_all('a', text = 'CSV')
url_city = 'https://data.gov.tw/dataset/7441'
shp_file, bool_list = [], []
for i, j in enumerate(os.listdir()):
    bool_list.append('shp' in j)
if True not in bool_list:
    soup_city = bs(io.StringIO(requests.get(url_city, stream = True, timeout = timeout).content.decode('utf-8')), 'html.parser')
    link_city = soup_city.find('a', text = 'SHP').get('href')
    with zf(io.BytesIO(requests.get(link_city, stream = True, timeout = timeout).content)) as file_city:
        file_city.extractall()
for i, j in enumerate(os.listdir()):
    if 'shp' in j:
        shp_file.append(j)
# convert data to array
table_array = np.array([])
for i, j in zip(range(0,len(titles_criminal),2), range(len(links_criminal))):
    table_array = np.append(table_array, [titles_criminal[i].text, links_criminal[j].get('href')])
# convert array to pandas
table_array = table_array.reshape(-1,2)
data = pd.DataFrame(table_array)
data.sort_values(by = data.columns[0], inplace = True)
data.reset_index(drop = 1, inplace = True)
# print gotten data
for i in range(int(len(data)/5)):
    print(str(i + 1) + "." + str(int(data[0][(i + 1) * 4][:3]) + 1911) + '年' + data[0][i * 4][-4:])
# show select data and read into pandas
data_index = int(input('which year do you want to show ? ')) - 1
print('you select: ' + str(data_index + 1) + "." + str(int(data[0][(i + 1) * 4][:3]) + 1911) + '年' + data[0][i * 4][-4:])
map_data = gp.read_file(shp_file[0], encoding = 'utf-8')
city = np.unique(map_data[map_data.columns[2]].values)
for i, j in enumerate(city):
    print(str(i + 1) + '.' +  j, end = ' ')
    if (i + 1) % 5 == 0:
        print()
city_index = int(input('\nwhich city do you want to query ? ')) -1
country_criminal = pd.DataFrame()
for i in range(4):
    country_criminal = country_criminal.append(pd.read_csv(io.StringIO(requests.get(data[1][data_index * 4 + i], stream = True, timeout = timeout).content.decode('utf-8'))))
city_criminal = country_criminal[country_criminal[country_criminal.columns[-1]].str.contains(city[city_index], na = False)]
city_criminal.rename(columns = {str(city_criminal.columns[1]):'date', str(city_criminal.columns[2]):'place'}, inplace = True)
city_criminal[city_criminal.type.str.contains(np.unique(city_criminal.type)[-1])]

# set plot and show
fig, ax = plt.subplots(1, 1)
map_data.plot(ax = ax, legend = True)
plt.show()