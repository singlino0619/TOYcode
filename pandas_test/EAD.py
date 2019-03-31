
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import seaborn as sns
get_ipython().magic('matplotlib inline')


# In[6]:


df_test = pd.read_csv('test.csv')


# In[7]:


df_test


# In[8]:


df_test['apply_PoE'] = df_test[['flg', 'PoE', 'CS_PoE']].apply(lambda x: x[2] if x[0] == 0 else x[1], axis=1)


# In[9]:


df_test[['flg', 'PoE', 'CS_PoE']].apply(lambda x: x[1], axis=1)


# In[10]:


df_aggregation_grid = pd.DataFrame(df_test.columns[6:-1])
df_aggregation_grid.head()


# In[11]:


for i in range(len(df_aggregation_grid)):
    df_test[df_aggregation_grid[0][i]] = df_test[['Maturity', 'apply_PoE']].apply(lambda x: x[1] if (str_to_dt_obj(x[0]) > str_to_dt_obj(df_aggregation_grid[0][i])) else 0, axis=1)


# In[12]:


df_test


# In[13]:


aggregation_grid = df_test.columns[6:]
len(aggregation_grid)


# In[14]:


for i in range(6, 6+len(aggregation_grid)):
    df_test[df_test.columns[i]] = 0


# In[15]:


pd.to_datetime(df_test['Maturity'])


# In[16]:


def str_to_dt_obj(str):
    return datetime.datetime.strptime(str, '%Y/%m/%d')


# ## 2019/3/26 EAD

# In[17]:


df_ead = pd.read_csv('EAD.csv')
df_ead


# In[18]:


def sort_values(g, str_sort):
    return g.sort_values(by=str_sort, ascending=False)


# In[19]:


df_ead.groupby('kbn').apply(sort_values, 'EAD_SACCR')


# In[20]:


df_ead.groupby(['kbn', 'gyousyu']).apply(sort_values, 'CEM_EAD')


# In[21]:


df_agg = df_ead.groupby(['kbn', 'gyousyu'], as_index=False).sum()
df_agg


# In[22]:


sns.barplot(data=df_agg, x='kbn', y='CEM_EAD')


# In[23]:


df_sum = df_ead.groupby('kbn', as_index=False).sum()
df_sum


# In[24]:


sns.countplot('kbn', data=df_ead)


# In[25]:


sns.set(style='darkgrid')
sns.pairplot(data=df_ead, x_vars='EAD_SACCR', y_vars='CEM_EAD', hue='kbn')


# In[26]:


sns.barplot(data=df_ead, x='kbn', y='EAD_SACCR', hue='gyousyu')


# In[27]:


sns.barplot(data=df_sum, x='kbn', y='EAD_SACCR')


# In[28]:


g = sns.FacetGrid(df_ead, col='gyousyu', hue='kbn')
g.map(plt.scatter, 'EAD_SACCR', 'CEM_EAD')


# In[29]:


mapping = {'bank': 1, 'ccp':2, 'customer': 3}
df_agg['kbn_num'] = df_agg['kbn'].apply(lambda x: mapping[x])
df_agg


# In[44]:


df_agg_agg = df_agg.groupby('kbn').sum().reset_index()
df_agg_agg


# In[103]:


#fig = plt.figure(figsize=(6,4))
#ax = fig.add_subplot(1,1,1)
width= 0.5
label = ['bank', 'ccp', 'customer']
plt.bar(df_agg['kbn_num'], df_agg['EAD_SACCR'], width=width, align='center')
plt.bar(df_agg['kbn_num']+width, df_agg['CEM_EAD'], width=width, align='center')

plt.xticks(df_agg['kbn_num'], label)


# In[381]:


def barplt_next_to_barplt(df, list_x_axis, list_y_axis, num_width):
    dict_y_axis = create_dict_for_barplt(df, list_y_axis)
    key_list = []
    value_list = []
    for key, values in dict_y_axis.items():
        key_list.append(key)
        value_list.append(values)
    len_x_axis = len(list_x_axis)
    num_list = np.arange(1, len_x_axis + 1)
    len_value_list = len(value_list)
    for i in range(len_value_list):
        plt.bar(num_list + num_width * i, value_list[i], width=num_width, align='center')
        plt.xticks( (2* (num_list - num_width) + num_width * len_value_list) / 2 , list_x_axis)
    plt.legend(key_list)


# In[382]:


def create_dict_for_barplt(df, y_axis_str_list):
    key_list = y_axis_str_list
    y_axis_dict = {}
    for i in range(len(y_axis_str_list)):
        y_axis_dict.setdefault(key_list[i], list(df[key_list[i]]))
    return y_axis_dict


# In[383]:


((np.arange(1,4) - 0.3) + (np.arange(1,4) - 0.3) + 0.3 * 3) /2


# In[384]:


for key, value in create_dict_for_barplt(df_agg_agg, ['EAD_SACCR', 'CEM_EAD', 'RWA_SACCR']).items():
    print(key)


# In[385]:


plt.figure(figsize=(10,6))
barplt_next_to_barplt(df_agg_agg, df_agg_agg['kbn'], ['EAD_SACCR', 'CEM_EAD'], 0.3)


# In[264]:


np.arange(1, 6)


# In[153]:


import matplotlib.pyplot as plt
import numpy as np
 
height1 = [80, 65, 100, 42, 54]  # 点数1
height2 = [55, 100, 98, 30, 21]  # 点数2
 
left = np.arange(len(height1))  # numpyで横軸を設定
labels = ['Japanese', 'Math', 'Science', 'Social', 'English']
 
width = 0.3
 
plt.bar(left, height1, color='r', width=width, align='center')
plt.bar(left+width, height2, color='b', width=width, align='center')
 
plt.xticks(left + width/2, labels)
plt.show()

