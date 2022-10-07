#!/usr/bin/env python
# coding: utf-8

# In[1]:


import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import os
import env

# In[ ]:
#get cohort tables from mysql
def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def get_cohort():
    filename = "cohort.csv"
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    else:
        # read the SQL query into a dataframe
        df = pd.read_sql('SELECT * FROM cohorts', get_connection('curriculum_logs'))

        # Write that dataframe to disk for later. Called "caching" the data for later.
        df.to_csv(filename,index=False)

        # Return the dataframe to the calling code
        return df

# acquire the data from local drive
#  create a function for it
# acquire the data from local drive
#  create a function for it
def acquire(file_name, column_names):
    cohort=get_cohort()
    df=pd.read_csv(file_name, sep="\s",
                       header=None,
                       names=column_names,
                       usecols=[0, 2, 3,4, 5])
    cohort=cohort.rename(columns={'id':'cohort_id'})
    df=pd.merge(cohort,df,on='cohort_id')
    df=df.drop(columns=['deleted_at'])
    return df
# In[18]:


# clean up the columns and set date to datetime
# change date to index
def prep(df):
    df.date = pd.to_datetime(df.date)
    df.start_date = pd.to_datetime(df.start_date)
    df.end_date = pd.to_datetime(df.end_date)
    df.updated_at = pd.to_datetime(df['updated_at']).dt.date
    df.created_at = pd.to_datetime(df['created_at']).dt.date
    df=df.dropna()
    return df


# In[ ]:




