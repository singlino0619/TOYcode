
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')


# In[4]:


from io import StringIO
import sqlite3
from sqlite3 import OperationalError


# # adhoc trial

# ## make, wirte and read DB for various base_date

# ### 20180928

# In[35]:


data = '''
GCIF,name,kbn,internal_rating
0111,SS,CUS,1
3890,JJ,IBK,2
8907,UH,CPP,3
7863,UK,CUS,6
'''
df_data_201809 = pd.read_csv(StringIO(data))
df_data_201809['base_date'] = '20180928'


# #### wirte sql

# In[36]:


dbname = '/Users/susynishida/Desktop/dev/DB/test/GCIF_LIST.db'
conn = sqlite3.connect(dbname)
df_data_201809.to_sql('GCIF_LIST_DB', conn, if_exists='append', index=False)
conn.close()


# #### read sql (do not forgett connect sqlite3 server)

# In[212]:


conn = sqlite3.connect(dbname)
pd.read_sql_query('SELECT * from GCIF_LIST_DB', conn)


# ### 20181228

# In[8]:


data = '''
GCIF,name,kbn,internal_rating
0234,BB,CUS,5
3330,JO,IBK,2
1127,IK,CPP,9
3843,KP,CUS,2
'''
df_data_201812 = pd.read_csv(StringIO(data))
df_data_201812['base_date'] = '20181228'


# #### wirte sql

# In[1]:


dbname = '/Users/susynishida/Desktop/dev/DB/test/GCIF_LIST.db'
conn = sqlite3.connect(dbname)
df_data_201812.to_sql('GCIF_LIST_DB', conn, if_exists='append', index=False)
conn.close()


# #### read sql

# In[40]:


conn = sqlite3.connect(dbname)
pd.read_sql_query('SELECT * from  GCIF_LIST_DB', conn)


# ## DELETE DB

# ###  Using where

# In[233]:


conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute("""DELETE from GCIF_LIST_DB where base_date='20181228'""")
conn.commit()


# ### All

# In[54]:


conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute("""DELETE from GCIF_LIST_DB""")
conn.commit()


# ## Create Table

# In[20]:


dbname = '/Users/susynishida/Desktop/dev/DB/test/GCIF_LIST.db'
conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute('CREATE table IF NOT EXISTS GCIF_LIST_DB(GCIF integer, name varchar(64), kbn varchar(64), internal_rating integer, base_date varchar(64))')
conn.commit()
conn.close()


# ## INSERT

# In[163]:


conn = sqlite3.connect(dbname)
cur = conn.cursor()
sql_command = 'INSERT into GCIF_LIST_DB (GCIF, name, kbn, internal_rating, base_date) values (?, ?, ?, ?, ?)'
values = (9873, 'CM', 'CUS', 3, '20180531')
cur.execute(sql_command, values)
conn.commit()


# In[24]:


conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute('SELECT * from GCIF_LIST_DB')
cur.fetchall()


# # define function: add_db by inputting base_date and show GCIF_LIST
# - 型はしっかり定義しないと予想と反する動きをする
# - 以下のコードで，str_base_dateはsqlの絡むでも文字列を想定しているが，何も設定しないとNONE型となり，
# - 抽出条件に引っかからなくなる
# - (コンピュータ的には)数値でも文字列でもない何かが入っており，こちらが指定しても反応してくれない．
# ```cur.execute("""SELECT * from {}""".format(table_name) + """ where base_date={}""".format(str_base_date))```

# In[103]:


# def add_db_GCIF_LIST(str_base_date, root_path, dbpath, table_name):
#     df_temp = pd.read_csv(root_path + '/GCIF_LIST_' + str_base_date +  '.csv')
#     df_temp['base_date'] = str_base_date
#     conn = sqlite3.connect(dbpath)
#     cur = conn.cursor()
#     cur.execute("""SELECT * from GCIF_LIST_DB where base_date={}""".format(str_base_date))
#     if(len(cur.fetchall()) == False):
#         print('This base date: ({}) '.format(str_base_date) + 'is new. Add database quickly.')
#         df_temp.to_sql(table_name, conn, if_exists='append', index=False)
#         conn.close()
#     else:
#         print('this base date: ({}) '.format(str_base_date) + 'is duplicated! Drop exsisting table and add new table.')
#         cur.execute("""DELETE from GCIF_LIST_DB where base_date={}""".format(str_base_date))
#         df_temp.to_sql(table_name, conn, if_exists='append', index=False)
#         conn.close()
    
def connect_GCIF_LIST(dbpath, table_name):
    conn = sqlite3.connect(dbpath)
    return pd.read_sql_query('SELECT * from {}'.format(table_name), conn)

def add_db_GCIF_LIST(str_base_date, root_path, dbpath, table_name):
    df_temp = pd.read_csv(root_path + '/GCIF_LIST_' + str_base_date +  '.csv')
    df_temp['base_date'] = str_base_date
    try:
        conn = sqlite3.connect(dbpath)
        cur = conn.cursor()
        cur.execute("""SELECT * from {}""".format(table_name) + """ where base_date='{}'""".format(str_base_date))
        if(len(cur.fetchall()) == 0):
            print('This base date: ({}) '.format(str_base_date) + 'is new. Add database quickly.')
            df_temp.to_sql(table_name, conn, if_exists='append', index=False)
            conn.close()
        else:
            print('this base date: ({}) '.format(str_base_date) + 'is duplicated! Drop exsisting table and add new table.')
            cur.execute("""DELETE from GCIF_LIST_DB where base_date='{}'""".format(str_base_date))
            df_temp.to_sql(table_name, conn, if_exists='append', index=False)
            conn.close()
    except OperationalError:
        print('no such table: {}'.format(table_name))
        sql_com_ct = 'CREATE table {}'.format(table_name) + '(GCIF int, name varchar(64), kbn varchar(64), internal_rating int, base_date varchar(64))'
        cur.execute(sql_com_ct) 
        conn.commit()
        conn.close()


# ## test function
# ### do

# In[106]:


root_path = '/Users/susynishida/Desktop/dev/DB_input/test'
dbpath = '/Users/susynishida/Desktop/dev/DB/test/GCIF_LIST.db'
table_name =  'GCIF_LIST_DB'
add_db_GCIF_LIST('20180928', root_path, dbpath, table_name)
add_db_GCIF_LIST('20181228', root_path, dbpath, table_name)
add_db_GCIF_LIST('20190329', root_path, dbpath, table_name)


# ### show DB

# In[107]:


dbpath = '/Users/susynishida/Desktop/dev/DB/test/GCIF_LIST.db'
table_name =  'GCIF_LIST_DB'
connect_GCIF_LIST(dbpath, table_name)


# ### test where (型のチェック)

# In[108]:


conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute("""SELECT * from {}""".format('GCIF_LIST_DB') + """ where base_date={}""".format(20181228))
print("""SELECT * from {}""".format('GCIF_LIST_DB') + """ where base_date={}""".format(20181228))
cur.fetchall()


# ## trial: add null base_date

# In[2]:


root_path = '/Users/susynishida/Desktop/dev/DB_input/test'
dbpath = '/Users/susynishida/Desktop/dev/DB/test/GCIF_LIST.db'
table_name =  'GCIF_LIST_DB'
df_20180630 = pd.read_csv(root_path + '/GCIF_LIST_' + '20180630.csv')
conn = sqlite3.connect(dbname)
df_20180630.to_sql(table_name, conn, if_exists='append', index=False)
connect_GCIF_LIST(dbpath, table_name)


# ### select null in base_date

# In[129]:


conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute("""SELECT * from GCIF_LIST_DB where base_date is null""")
cur.fetchall()


# ### delete null in base_date
# - executeするときは必ずcommitする!!

# In[139]:


conn = sqlite3.connect(dbname)
cur = conn.cursor()
cur.execute("""DELETE from GCIF_LIST_DB where base_date IS NULL""")
conn.commit()

