import pandas as pd 
import seaborn as sb 
import matplotlib.pyplot as plt
from scipy import stats ## this liibrary is used for using statistical functions

data = pd.read_csv(r'D:\retail-sales-analytics\salesAnalytics\Sample - Superstore.csv', encoding='ISO-8859-1')
print(data.head()) ## this step is done to see whether the data is loaded correrctly or not

print(data.info())

# now we will turn the data into a correlation matrix of heatmap
num_data = data.select_dtypes(include='number') ## this helps in including only numeric data
correlation_matrix = num_data.corr() ## this turns the data into correlation matrix mraniing a square matrix inform of i,j
print(correlation_matrix)
plt.figure(figsize = (7,7)) ## helps to figure the size of matrix
sb.heatmap(correlation_matrix,annot=True,cmap='coolwarm') ##converts matrix into heatmap matrix
plt.title("Correlational Maatrix") ##Gives the title of matrix
plt.show() ## to dispay the matrix