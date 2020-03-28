import geopandas as gp
import pandas as pd
import bs4
import requests
import numpy as np
import io
from bs4 import BeautifulSoup as bs
# get data
url = 'https://data.gov.tw/dataset/14200'
soup = bs(io.StringIO(requests.get(url).content.decode('utf-8')), 'html.parser')
titles = soup.find_all('span', class_ = 'ff-desc')
links = soup.find_all('a', text = 'CSV')
# convert data to array
table_array = np.array([])
for i, j in zip(range(0,len(titles),2), range(len(links))):
    table_array = np.append(table_array, [titles[i].text, links[j].get('href')])
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
country_criminal = pd.DataFrame()
for i in range(4):
    country_criminal = country_criminal.append(pd.read_csv(io.StringIO(requests.get(data[1][data_index * 4 + i]).content.decode('utf-8'))))
city_criminal = country_criminal[country_criminal[country_criminal.columns[-1]].str.contains('彰化', na = False)]
city_criminal.rename(columns = {str(city_criminal.columns[1]):'date', str(city_criminal.columns[2]):'place'}, inplace = True)
print(city_criminal)
print(city_criminal.groupby(city_criminal.columns[-1]).count())