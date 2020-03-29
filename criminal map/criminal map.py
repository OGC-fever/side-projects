import geopandas as gp
import pandas as pd
import bs4, requests
import numpy as np
import io ,os
from bs4 import BeautifulSoup as bs
from zipfile import ZipFile
import matplotlib.pyplot as plt
# get criminal data
url_criminal = 'https://data.gov.tw/dataset/14200'
soup_criminal = bs(io.StringIO(requests.get(url_criminal).content.decode('utf-8')), 'html.parser')
titles_criminal = soup_criminal.find_all('span', class_ = 'ff-desc')
links_criminal = soup_criminal.find_all('a', text = 'CSV')
# get city data and unpack zipfile
url_city = 'https://data.gov.tw/dataset/7441'
soup_city = bs(io.StringIO(requests.get(url_city).content.decode('utf-8')), 'html.parser')
link_city = soup_city.find('a', text = 'SHP').get('href')
# with ZipFile(io.BytesIO(requests.get(link_city).content)) as file_city:
#     for i in range(len(file_city.infolist())):
#         print(file_city.infolist()[i])
#     file_city.extractall()
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
# set plot
fig, ax = plt.subplots(1, 1)
map_data = gp.read_file(shp_files[-1])
map_data.plot(ax = ax, legend = True)
plt.show()
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
city_index = int(input('which city do you want to show ? ')) - 1
country_criminal = pd.DataFrame()
for i in range(4):
    country_criminal = country_criminal.append(pd.read_csv(io.StringIO(requests.get(data[1][data_index * 4 + i]).content.decode('utf-8'))))
city_criminal = country_criminal[country_criminal[country_criminal.columns[-1]].str.contains('彰化', na = False)]
city_criminal.rename(columns = {str(city_criminal.columns[1]):'date', str(city_criminal.columns[2]):'place'}, inplace = True)
print(city_criminal.groupby(city_criminal.columns[-1]).count())
print(city_criminal.groupby(city_criminal.columns[0]).count())