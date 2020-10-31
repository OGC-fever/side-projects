from .getdata import *

url2 = link[0:4]
page2, soup2, img_url, pic = [], [], [], []
for i in range(len(url2)):
    page2.append(requests.get(url2[i]))
    soup2.append(bs(page2[i].content,'lxml'))
    img_url.append(soup2[i].find_all('meta', {'name':"twitter:image"})[0]["content"])
    pic.append(np.array(Image.open(BytesIO(requests.get(img_url[i]).content))))