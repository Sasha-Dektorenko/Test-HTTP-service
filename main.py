import pandas as pd
a = pd.read_csv("static/dictionary.csv", encoding='utf-8', sep='\t')
#a = pd.read_excel("static/new_excel.xlsx", sheet_name = "Лист1")
print(a.iloc[0:2, 1])