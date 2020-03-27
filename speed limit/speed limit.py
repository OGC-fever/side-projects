url = 'https://www.chpb.gov.tw/uploaddowndoc?file=infopublic/201905291540240.csv&filedisplay=%E5%BD%B0%E5%8C%96%E7%B8%A3%E8%AD%A6%E5%AF%9F%E5%B1%80%E6%89%80%E5%B1%AC%E5%90%84%E8%BE%A6%E5%85%AC%E8%99%95%E6%89%80%E6%A0%B8%E5%BF%83%E5%8F%8A%E4%B8%80%E8%88%AC%E8%A8%AD%E6%96%BD%E9%85%8D%E7%BD%AE%E8%A1%A81080528.csv&flag=doc'

import pandas as pd

data = pd.read_csv(url, encoding = 'big5')
print(data.head())