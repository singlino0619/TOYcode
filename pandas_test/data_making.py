
# coding: utf-8

# In[519]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')
import seaborn as sns
from io import StringIO


# In[520]:


data_columns = ['grid', 'pair', 'final', 'csa', 'rcv_rate', 'pay_rate', 'rat_1', 'rat_2', 'rat_3']


# In[521]:


data = """
012M,USD_JPY,1,0,fix,fix
024M,USD_JPY,1,0,fix,fix
036M,USD_JPY,1,0,fix,fix
012M,USD_JPY,1,0,floot,fix
024M,USD_JPY,1,0,floot,fix
036M,USD_JPY,1,0,floot,fix
012M,USD_JPY,0,0,fix,fix
024M,USD_JPY,0,0,fix,fix
036M,USD_JPY,0,0,fix,fix
012M,USD_JPY,0,0,floot,fix
024M,USD_JPY,0,0,floot,fix
036M,USD_JPY,0,0,floot,fix
"""
df_test = pd.read_table(StringIO(data), sep=',', header=None, names=data_columns)


# In[522]:


df_test['final'] = df_test['final'].astype('str')
df_test['csa'] = df_test['csa'].astype('str')
df_test


# In[523]:


StringIO(data).getvalue()


# In[524]:


df_test['rat_1'] = np.random.rand(len(df_test))
df_test['rat_2'] = np.random.rand(len(df_test))
df_test['rat_3'] = np.random.rand(len(df_test))


# In[525]:


df_test['key'] = df_test.apply(lambda x: '_'.join(x[0:6]) ,axis=1)
df_test.head()


# In[526]:


columns_list = list(df_test.columns[6:9])
columns_list


# In[527]:


df_test['rate'] = columns_list[0]
df_test['value'] = df_test.apply(lambda x: x['rat_1'], axis=1)
df_test


# In[528]:


copy_len = len(columns_list)
for i in range(copy_len - 1):
    df_test_temp = df_test.copy()
    df_test_temp['rate'] = columns_list[i + 1]
    df_test_temp['value'] = df_test_temp.apply(lambda x: x[columns_list[i + 1]], axis=1)
    df_test = df_test.append(df_test_temp)


# In[532]:


df_test.head(20)


# In[607]:


grid_mapping = {'012M': 1, '024M': 2, '036M': 3}


# In[613]:


df_test['grid_year'] = df_test['grid'].apply(lambda x: grid_mapping[x])
df_test.head()


# In[623]:


df_test['rate_type'] = df_test.apply(lambda x: '_'.join(x[4:6]), axis=1)
df_test.head(10)


# In[631]:


rating_mapping = {'rat_1': 1, 'rat_2': 2, 'rat_3': 3}
df_test['rate_num'] = df_test['rate'].apply(lambda x: rating_mapping[x])
df_test


# In[632]:


grid = sns.FacetGrid(df_test, row='pair', col='rate_type', hue='final')
grid.map(plt.plot, 'rate_num', 'value')

