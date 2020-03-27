url = 'https://data.fda.gov.tw/opendata/exportDataList.do?method=ExportData&InfoId=21&logType=5'

import pandas as pd

data = pd.read_json(url)
print(data.head())