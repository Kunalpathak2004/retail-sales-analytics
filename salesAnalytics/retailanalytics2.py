import pandas as pd 
import seaborn as sb 
import matplotlib.pyplot as plt
from scipy import stats ## this liibrary is used for using statistical functions

# cleaning the data
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

# converting data types
data.dropna(inplace=True)
data['Order Date'] = pd.to_datetime(data['Order Date'])## this converts the data type of order data into date time data type
print(data.info())

# putting month and year o order date
data['month'] = data['Order Date'].dt.month
data['year'] = data['Order Date'].dt.year
print(data.head())

# describing the data
print(data.describe())

# performing exploratory data analysis (EDA)
# a) using time series charts like axis graphs
monthly_sales = data.groupby(['year', 'month'])['Sales'].sum().reset_index() ##this line groups the data into year and month and sums thier values and then resets it do that we can plot it properly
print("::m", monthly_sales)
plt.figure(figsize=(14,7))
sb.lineplot(data=monthly_sales, x="month", y="Sales", hue="year")
plt.title("Monthly Sales Report")
plt.show()
print(monthly_sales) 
# from this we get a line chart
# b) using bar and pie chart
plt.figure(figsize=(12,6))
sb.barplot(data=data, x ='Category', y='Sales', hue='Region')
plt.title('Category wise Sales by Region')
plt.show()

region_sales = data.groupby('Region') ['Sales'].sum()
plt.pie(region_sales,labels=region_sales.index,autopct='%1.1f%%')
plt.title('Sales by Region')
plt.show()
# c) Scatter plot
plt.figure(figsize=(8,6))
sb.scatterplot(data=data, x='Sales',y='Profit',hue='Segment')
plt.title("Sales vs Profit by Customer Segment")
plt.show()


# d) performance analysis
data.columns = data.columns.str.strip()
# print(data.columns.tolist())
product_performance = data.pivot_table(values='Sales',index='Category',columns='Sub-Category',aggfunc='sum')
plt.figure(figsize=(12,8))
sb.heatmap(product_performance,cmap='YlGnBu')
plt.title('Product Performance Heatmap')
plt.show()

# e) Hypothesis testing and statistical analysis
region1 = 'East'
region2 = 'South'

threshold = 0.05
region1_sales = data[data['Region'] == region1] ['Sales']
region2_sales = data[data['Region'] == region2] ['Sales']
t_stat, p_val = stats.ttest_ind(region1_sales, region2_sales)
print(f'p-value = {p_val}')

if(p_val < threshold):
    print("Reject null hypothesis, there is significant difference between two regions")
elif(p_val > threshold):
    print("Did not reject null hypothesis, there is no significant difference between two regions")

print(data)
print(num_data.corr())
print(data.describe())

sb.histplot(data=data, x='Discount', bins=20, kde=True)