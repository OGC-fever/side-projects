import pandas as pd
url = 'https://www.water.gov.tw/opendata/qual5.csv'
hardness = pd.read_csv(url)
print(hardness.head())