import pandas as pd

file = 'sample/B-KPV NRC LIST (2 Oct).xls'
xlsx = pd.ExcelFile(file)
print(xlsx)
