import pandas as pd
import bs4
import requests
import numpy as np
from bs4 import BeautifulSoup as bs
# get data
url = 'https://data.gov.tw/dataset/14200'
soup = bs(requests.get(url).content, 'html.parser')
titles = soup.find_all('span', class_ = 'ff-desc')
links = soup.find_all('a', text = 'CSV')
# bs.element_classes.
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
for i in range(len(data)):
    print(str(i + 1) + "." + data[0][i])
# show select data and read into pandas
data_index = int(input('which data do you want to show ? ')) - 1
print('you select: ' + str(data_index + 1) + "." + data[0][data_index])
url = data[1][data_index]
# select_soup = bs(requests.get(url).content, 'html.parser')
# temp = pd.read_json(str(select_soup))
temp = pd.read_csv(url)
# season_criminal = pd.DataFrame(temp[temp.columns[1]][2])
county_criminal = temp[temp[temp.columns[-1]].str.contains('彰化', na = False)]
county_criminal.rename(columns = {str(county_criminal.columns[1]):'date' ,str(county_criminal.columns[2]):'location'}, inplace = True)
print(county_criminal)
county_criminal.groupby()