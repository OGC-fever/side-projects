import pandas as pd
import bs4
import requests
import numpy as np

url = 'https://data.gov.tw/dataset/14200'
req = requests.get(url)
soup = bs4.BeautifulSoup(req.content, 'html.parser')
titles = soup.find_all('span', class_ = 'ff-desc')
links = soup.find_all('a', class_ = 'dgresource', title = "下載格式為 CSV")

table_array = []
for i, j in zip(range(0,len(titles),2), range(len(links))):
    table_array.append([titles[i].text, links[j].text])

table_array = np.array(table_array)
data = pd.DataFrame(table_array)
data.sort_values(by = data.columns[0], inplace = True)
data.reset_index(drop = 1, inplace = True)

for i in range(len(data)):
    print(str(i + 1) + "." + data[0][i])

data_index = int(input('which data do you want to show ? ')) - 1
20
print('you select: ' + str(data_index + 1) + "." + data[0][data_index])
url = data[1][data_index]
criminal_data = pd.read_csv(url)
county_criminal = criminal_data[criminal_data[criminal_data.columns[-1]].str.contains('彰化', na = False)]
county_criminal.rename(columns = {str(county_criminal.columns[1]):'date' ,str(county_criminal.columns[2]):'location'}, inplace = True)
print(county_criminal)