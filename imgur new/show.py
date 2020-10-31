from packages.showdata import *

img_hight = 5
fig, ax = plt.subplots(1, len(url2))
fig.set_tight_layout("tight")
fig.set_size_inches(img_hight * len(url2), img_hight)
for i in range(len(url2)):
    plt.imshow(pic[i])
    ax[i].set_axis_off()
    ax[i].imshow(pic[i])
plt.show()