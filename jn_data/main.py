import numpy
import pandas
import matplotlib.pyplot as plt

### 读取csv
a = pandas.read_csv("./Crime_Statistics_SA_2014_2019.csv",delimiter=",")


## 1
#print(a.shape) # (385296, 7) 不包含首行

## 2
#print(a.isnull().any()) # 缺失值所在列
#print(a[a.isnull().values==True]) # 获得缺失值的准确位置

## 3
# print(a['Reported Date'].dtypes)
a['Reported Date'] = pandas.to_datetime(a['Reported Date'], format ='%Y-%m-%d')
# print(a['Reported Date'].dtypes)
# print(a['Reported Date'].max())
# print(a['Reported Date'].min())

## 4

# current_col= a['Offence Count']
# print(current_col.count()) # 不包含首行
# print(current_col.mean()) # 平均值
# print(current_col.std()) # 标准差
# print(current_col.max()) # 最大值
# print(current_col.min()) # 最小值

# ## 5
# current_col = a['Offence Level 1 Description']
# ## 5.1
# print(len(current_col.unique())) # 唯一值列表长度
# ## 5.2
# print(current_col.unique()) # 唯一值列表
# ## 5.3
# print(current_col.value_counts()['OFFENCES AGAINST THE PERSON'])
# ## 5.4
# print(current_col.value_counts()['OFFENCES AGAINST PROPERTY']/current_col.size)

## 6

## 6.1
current_col = a['Offence Level 2 Description']
print(current_col.value_counts()) # 唯一值列表长度

## 6.2
current_col = a[(a['Offence Count'] > 1) & (a['Offence Level 2 Description'] == "SERIOUS CRIMINAL TRESPASS")]
print(len(current_col))



### task B


## 1

# counts = a['Reported Date'].groupby(a['Reported Date'].dt.year).count()
# # a['Reported Date'].dt.year.hist()
# # a['year'] = a['Reported Date'].dt.year
# # #a['year'].hist(by=None,bins=6)
# # a['year'].hist(align="left",bins=range(2014,2021))
# counts.plot(kind="bar")
# plt.xticks(rotation=360)
# plt.title("Investigating the number of crimes per year")
# plt.xlabel("year")
# plt.ylabel("times")
# plt.show()

## 2

# 2.1
# ??
current_col = a['Suburb - Incident']
c = current_col.groupby(current_col)
counts = c.count()
counts.plot()
sort_v = counts.sort_values()
print(sort_v.mean())
print(sort_v.median())
#plt.show()


# 2.2 
## ?? 

# new_counts = counts[counts >= 5000]
# new_counts.plot(kind="bar",fontsize = 6)
# plt.xticks(rotation=360)
# plt.xlabel("suburb")
# plt.ylabel("times")
# plt.title("suburbs's total number of crimes are greater than 5000")
# plt.show()



## 3
# mt15_col = a[a['Offence Count'] > 15]
# #print(mt15_col)
# c = mt15_col['Suburb - Incident'].groupby(mt15_col['Suburb - Incident']).count()
# c.plot(kind="bar")
# print(c)
# plt.xticks(rotation=360)
# plt.xlabel("suburb")
# plt.ylabel("times")
# plt.show()


## 3.2
## ??
# print(a.describe())
# a[a['Offence Count'] > 12].boxplot("Offence Count")
# plt.show()
# # drop 

####