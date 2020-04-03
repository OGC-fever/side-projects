import geopandas as gp
import pandas as pd
import bs4, requests, io, os
import numpy as np
from bs4 import BeautifulSoup as bs
from zipfile import ZipFile as zf
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patheffects as pe
import matplotlib.colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
# get data
url = 'https://www.water.gov.tw/opendata/qual5.csv'
hardness = pd.read_csv(url)
url_city = 'https://data.gov.tw/dataset/7441'
soup_city = bs(io.StringIO(requests.get(url_city, stream = True, timeout = 3).content.decode('utf-8')), 'html.parser')
link_city = soup_city.find('a', text = 'SHP').get('href')
# get city data and unpack zipfile, del unused files
del_files, shp_file, bool_list = [], [], []
for i, j in enumerate(os.listdir()):
    bool_list.append('shp' in j)
if True not in bool_list:
    with zf(io.BytesIO(requests.get(link_city, stream = True, timeout = 3).content)) as file_city:
        file_city.extractall()
for i, j in enumerate(os.listdir()):
    if 'TOWN' not in j:
        if 'py' not in j:
            del_files.append(j)
    elif 'shp' in j:
        shp_file.append(j)
for i, j in enumerate(del_files):
    os.remove(del_files[i])
# read/filter/select city hardness and map, combine together
map_data = gp.read_file(shp_file[0], encoding = 'utf-8')
city = np.unique(hardness[hardness.columns[0]].values)
for i, j in enumerate(city):
    print(str(i + 1) + '.' +  j, end = ' ')
    if (i + 1) % 5 == 0:
        print()
city_index = int(input('\nwhich city do you want to query ? ')) -1
print('you select : ' + str(city_index + 1) + '.' + city[city_index])
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
fig, ax = plt.subplots(figsize = (10, 10))
step = 5
level = 300 / step
norm = matplotlib.colors.BoundaryNorm(np.arange(0, 301, level), step)
cmap = plt.get_cmap('RdYlGn_r', step)
show = plot_data.plot(column = plot_data[plot_data.columns[-1]], ax = ax, cmap = cmap, edgecolor = 'black', linewidth = 1, norm = norm)
for i in range(len(plot_data)):
    show.annotate(s = plot_data[plot_data.columns[1]][i], xy = (plot_data.centroid.x[i], plot_data.centroid.y[i]), ha = 'center', va = 'center', fontsize = 'large', color = 'black', path_effects = [pe.withStroke(linewidth = 2, foreground = 'white')])
plt.axis('equal')
ax.axis('off')
ax.set_title(city[city_index] + "自來水硬度", fontsize = 'x-large')
plt.tight_layout()
colors = list(map(cmap, range(step)))
handles = [plt.Rectangle((0, 0), 3, 6, facecolor = c, edgecolor = 'black', linewidth = 0.5) for c in colors]
labels = ["0~60:軟水", "61~120:中等軟水", "121~180:硬水", ">181:超硬水", ">241:你在喝沙?"]
leg = ax.legend(handles, labels, loc = 0, prop = {'size':'large'})
leg.set_title(title = '硬度:mg/L', prop = {'size':'large'})
plt.show()
