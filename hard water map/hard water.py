import geopandas as gp
import pandas as pd
import bs4, requests, io, os
import numpy as np
from bs4 import BeautifulSoup as bs
from zipfile import ZipFile as zf
import matplotlib.pyplot as plt
import matplotlib as mpl

# get hardness data
url = 'https://www.water.gov.tw/opendata/qual5.csv'
hardness = pd.read_csv(url)
# print(hardness.head())
# get city data and unpack zipfile, del unused files
url_city = 'https://data.gov.tw/dataset/7441'
soup_city = bs(io.StringIO(requests.get(url_city, stream = True, timeout = 5).content.decode('utf-8')), 'html.parser')
link_city = soup_city.find('a', text = 'SHP').get('href')
del_files, shp_files, bool_list = [], [], []
for i, j in enumerate(os.listdir()):
    bool_list.append('shp' in j)
while True not in bool_list:
    with zf(io.BytesIO(requests.get(link_city, stream = True, timeout = 5).content)) as file_city:
        file_city.extractall()
for i, j in enumerate(os.listdir()):
    if 'TOWN' not in j:
        if 'py' not in j:
            del_files.append(j)
    elif 'TOWN' in j:
        shp_files.append(j)
for i, j in enumerate(del_files):
    os.remove(del_files[i])
# read/filter/select city hardness and map, combine together
city = np.unique(hardness[hardness.columns[0]].values)
for i, j in enumerate(city):
    print(str(i + 1) + '.' +  j, end = ' ')
    if (i + 1) % 5 == 0:
        print()
city_index = int(input('\nwhich city do you want to query ? ')) -1
print('you select : ' + str(city_index + 1) + '.' + city[city_index])
map_data = gp.read_file(shp_files[-1], encoding = 'utf-8')
city_data = hardness[hardness[hardness.columns[0]].str.contains(city[city_index])]
city_data.sort_values(by = city_data.columns[1], inplace = True)
city_data.reset_index(drop = 1, inplace = True)
city_map = map_data[map_data[map_data.columns[2]].str.contains(city[city_index])]
city_map.drop(city_map.columns[[0,1,4,5,6]], axis = 1, inplace = True)
city_map.sort_values(by = city_map.columns[1], inplace = True)
city_map.reset_index(drop = 1, inplace = True)
plot_data = city_map.join(city_data)
plot_data.drop(plot_data.columns[[-2, -3]], axis = 1, inplace = True)
# set plot and show
mpl.rcParams['font.sans-serif'] = ['Noto Sans CJK JP']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = "sans-serif"
fig, ax = plt.subplots()
show = plot_data.plot(column = plot_data[plot_data.columns[-1]], ax = ax, legend = True, cmap = plt.get_cmap('RdYlGn_r', 5), edgecolor = 'k', linewidth = 1, norm = plt.Normalize(vmin = 0, vmax = 300))
for i in range(len(plot_data)):
    show.annotate(s = plot_data[plot_data.columns[1]][i], xy = (plot_data.centroid.x[i], plot_data.centroid.y[i]), ha = 'center', fontsize = 12)
plt.axis('equal')
ax.set_axis_off()
ax.set_title(city[city_index] + "自來水硬度", fontsize = 16)
plt.tight_layout()
plt.show()
