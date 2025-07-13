import pandas as pd 
import seaborn as sb 
import matplotlib as plt
from scipy import stats ## this liibrary is used for using statistical functions

data = pd.read_csv(r'D:\retail-sales-analytics\salesAnalytics\Sample - Superstore.csv', encoding='ISO-8859-1')
print(data.head()) ## this step is done to see whether the data is loaded correrctly or not