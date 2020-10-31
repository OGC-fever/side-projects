import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

csv = "https://quality.data.gov.tw/dq_download_csv.php?nid=33604&md5_url=81f4c643c598f4cb945d752025b56909"
data = pd.read_csv(csv)
new_data = pd.DataFrame(data[data.columns[0:2].append(data.columns[3:])])

loop_tool = new_data[new_data.columns[2:]].values.shape
temp_array = new_data[new_data.columns[2:]].values
for i in range(loop_tool[0]):
    for j in range(loop_tool[1]):
        temp_array[i][j] = str(temp_array[i][j])
        temp_array[i][j] = temp_array[i][j].replace(",", "")
        temp_array[i][j] = int(temp_array[i][j])
new_data[new_data.columns[2:]] = pd.DataFrame(temp_array)
plot_data = new_data[new_data.columns[2:]]

ratio = []
for i in range(int(len(plot_data.index)/2)):
    for j in range(len(plot_data.columns)):
        try:
            ratio.append(plot_data.iloc[i*2][j]/plot_data.iloc[i*2+1][j])
        except:
            ratio.append(0)
ratio = np.array(ratio).reshape(-1, len(plot_data.columns))

add_array = []
for i in range(2):
    add_array.append(list(range(i, int(len(plot_data.index)/2), 2)))

total_ratio = [[], []]

for i in range(2):
    total_ratio[i] = plot_data.iloc[add_array[i]].sum()
total_ratio = total_ratio[0]/total_ratio[1]
total_ratio = list(total_ratio)


def show_town():
    for i in range(int(len(new_data[new_data.columns[0]])/2)):
        town.append((new_data[new_data.columns[0]].values[i*2]))
    for i in range(len(town)):
        if (i+1) % 7 != 0:
            print(str(i) + " " + town[i], end=' ')
        else:
            print(str(i) + " " + town[i])

plt.figure()
plt.rcParams['font.sans-serif'] = ['Noto Sans CJK JP', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = "sans-serif"
plt.rcParams.update({'font.size': 14})
town = []
show_town()
# select_town=int(input("\nwhich one to show?\n"))-1
'''
0 彰化市 1 員林市 2 鹿港鎮 3 和美鎮 4 北斗鎮 5 溪湖鎮 6 田中鎮
7 二林鎮 8 線西鄉 9 伸港鄉 10 福興鄉 11 秀水鄉 12 花壇鄉 13 芬園鄉
14 大村鄉 15 埔鹽鄉 16 埔心鄉 17 永靖鄉 18 社頭鄉 19 二水鄉 20 田尾鄉
21 埤頭鄉 22 芳苑鄉 23 大城鄉 24 竹塘鄉 25 溪州鄉
'''
select_town = 22
plt.title("彰化縣男女比率/年齡分佈", fontsize='x-large')
plt.plot(total_ratio, 'C0-.', label='彰化縣')
plt.plot(ratio[select_town], 'C1-.', label=town[select_town])
plt.axhline(y=1, color='gray')
plt.legend(loc=0)
plt.grid()
plt.xticks(range(0, 101, 10))
plt.xlabel("age")
plt.ylabel("male/female ratio")
plt.show()
