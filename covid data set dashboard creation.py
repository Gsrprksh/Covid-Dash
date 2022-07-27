#!/usr/bin/env python
# coding: utf-8

# In[236]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn
pd.pandas.set_option('max_columns',500)
pd.pandas.set_option('max_rows',500)
import requests
from bs4 import BeautifulSoup


# In[237]:


# now lets get the dataframe by scrapping the data using requests library
url = 'https://www.worldometers.info/coronavirus/'
# lets get the data using requests library

x = requests.get(url)
x


# In[238]:


# response 200 means that the data can be scrapped.

# lets parse the data into 'lxml' format.
# for that we can use the beautiful soup library.

soup = BeautifulSoup(x.content,'lxml')


# In[239]:


soup


# In[240]:


# now, we do have the data in our desired format.
# lets focus on extracting the table data where we can have all the countries information
# lets create an variable with an empty list for storing our information followed by  converting that into a data frame

frame1 =[]
a = soup.find('table')
for row in a.find_all('tr'):
    col = row.find_all('td')
    col = [ele.text.strip() for ele in col]
    frame1.append(col)


# In[241]:


frame1


# In[242]:


# lets convert the above list of lists into data frame followed by cleaning the data.
df = pd.DataFrame(frame1)


# In[243]:


df


# In[244]:


df = df.iloc[8:,:]


# In[245]:


df


# In[246]:


df2 = df.iloc[:,:15]


# In[247]:


df2.head()


# In[248]:


# lets give a column name to each column.
columns = ['count','country','total_cases','new_cases','total_deaths','new_deaths','total_recovered','new_recovered','active_cases','serious','total_cases/1mp','deaths/1mp','total_tests','tests/1mp','population']
df2.columns = columns


# In[249]:


df2.head()


# In[250]:


# lets consider only the columns which will be useful for our dashboard.
# country
# total_cases
# total_deaths
# total_recoverd
# active_cases
# serious
# total_cases/1mp
# deaths/1mp
# total_tests
# tests/1mp
# population


# In[251]:


df2 = df2[['total_cases','total_deaths','total_recovered','active_cases','serious','total_cases/1mp','deaths/1mp','total_tests','tests/1mp','population']]


# In[252]:


df2


# In[253]:


df2.info()


# In[254]:


df2.isnull().sum()


# In[255]:


# 1st problem- there are some places that are empty. we have to fill them or remove that entire column.
# 2nd problem- the numerical values are seperated with commas. we have to take the commos off.
# 3rd problem- despite all columns are numeric the data types were as an object. we have to change them to int type.


# In[256]:


country = df[1]


# In[257]:


df2['country'] = country


# In[258]:


df2.head()


# In[ ]:





# In[259]:



X = df2.loc[df2['country']== 'USA'] 


# In[260]:


X['population'] = '331,002,651'


# In[261]:


X


# In[262]:


df2.drop(index = 9, axis = 0, inplace = True)


# In[263]:


df2


# In[264]:


df2 = pd.concat([df2, X], axis = 0)


# In[265]:


# before sorting all the values we have to convert all of them into data type int 64.


# In[266]:


df2


# In[267]:


df2.drop(columns ='serious', axis = 1, inplace = True)


# In[268]:


df2 = df2.loc[(df2['active_cases']!= 'N/A') | (df2['total_recovered']!= 'N/A')]


# In[269]:


df2


# In[ ]:





# In[270]:


df2['total_cases'] =df2['total_cases'].str.replace(',','').astype('int64')


# In[271]:


def convert(x,df):
    for i in range(1,len(x)):
        df[i] = df[x[i]].str.replace(',','').astype('int64')
    return df
    


# In[272]:


x1 = df2.drop(columns='country',axis = 1)


# In[273]:


df2 = df2.sort_values(ascending = False, by = 'total_cases')


# In[274]:


df2.index


# In[275]:


df3 =[]
for i,j in enumerate(df2.index):
    if j <= 200:
        df4 = df2.iloc[i]
        df3.append(df4)
        


# In[276]:


df3 = pd.DataFrame(df3)


# In[277]:


df2 = df3.sort_values(ascending = False, by = 'total_cases')


# In[278]:


columns = x1.columns


# In[279]:


columns


# In[280]:


df2


# In[281]:


df2.drop(index = 8, axis = 0, inplace = True)


# In[282]:


df2 =df2.reset_index()


# In[283]:


df2.head()


# In[284]:


df2.drop(columns = 'index', axis = 1, inplace = True)


# In[285]:


df2.head()


# In[286]:


df2.drop(columns = ['total_cases/1mp','deaths/1mp','tests/1mp'], axis = 1, inplace = True)


# In[287]:


df2


# In[288]:


df2['total_deaths'] =df2['total_deaths'].str.replace(',','').astype('int64')


# In[289]:


df2['total_recovered'] =df2['total_recovered'].str.replace(',','').astype('int64')


# In[290]:


df2['active_cases'] =df2['active_cases'].str.replace(',','').astype('int64')


# In[291]:


df2


# In[292]:


df2.drop(index =[23,143],axis = 0, inplace = True)


# In[293]:


df2


# In[294]:


df2.drop(index =[142,168,166],axis = 0, inplace = True)


# In[295]:


df2 = df2.reset_index()


# In[296]:


df2.drop(columns = 'index',axis =1, inplace = True)


# In[300]:



df2['total_tests'] =df2['total_tests'].str.replace(',','').astype('int64')


# In[299]:


df2['population'] = df2['population'].str.replace(',','').astype('int64')


# In[301]:


df2


# In[302]:


# now we do have cleaned data.
# lets write the points to which we have to create a chart.
# total_cases
# total_deaths
# total_recoverd
# total_tests
# total_cases with respect to population
# bar chart for describing the total cases in each country.
# percentage of death
# percentage of recovery


# In[303]:


df2


# In[304]:


# lets add some more columns

df2['td/tc'] = df2['total_deaths']/df2['total_cases']


# In[305]:


df2['td/tr'] = df2['total_recovered']/df2['total_cases']


# In[306]:


df2


# In[307]:


df2.to_csv('df2.csv')


# In[308]:


df


# In[309]:


df.drop(index = 8,axis = 0, inplace = True)


# In[310]:


df


# In[311]:


df1 = pd.DataFrame()
df1['country'] = df[1]
df1['continent'] = df[15]


# In[312]:


df1


# In[313]:


df1.index = df1['country']


# In[314]:


df1


# In[315]:


df1.drop(columns = 'country',axis = 1,inplace = True)


# In[316]:


df1 = df1.reset_index()


# In[317]:



df2 = df2.merge(df1, on = 'country')


# In[318]:


df2 


# In[319]:


df2.to_csv('covid1.csv')


# In[320]:


url = 'https://www.iban.com/country-codes'


# In[321]:


import requests


# In[322]:


x = requests.get(url)


# In[323]:


y = BeautifulSoup(x.content, 'lxml')


# In[330]:


z = []
z1 = y.find('table')
for row in z1.find_all('tr'):
    col = row.find_all('td')
    col = [ele.text.strip() for ele in col]
    z.append(col)


# In[331]:


df1 = pd.DataFrame(z)


# df1

# In[332]:


df1


# In[336]:


df1.drop(columns = 3, inplace = True, axis = 1)


# In[337]:


columns = ['country','code1','code2']


# In[338]:


df1.columns = columns


# In[339]:


df1


# In[344]:


df3 = df2.merge(df1, on = 'country')


# In[345]:


df3.to_csv('df3.csv')


# In[346]:


df1.index = df1['country']


# In[347]:


df1


# In[368]:





# In[367]:


df2['code'] = np.where(df2['country']!= np.nan,1,0)


# In[ ]:





# In[ ]:





# In[369]:


df2.index = df2['country']


# In[ ]:





# In[ ]:




