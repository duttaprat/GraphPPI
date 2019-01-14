
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import math


# In[32]:


all_data = pd.read_csv("dataset/GDS3268.txt", sep="\t", header=None)
# data_list_of_list = pd.read_csv("McTwo/GDS4206.txt", sep="\n", header=None).values.tolist()
# selected_gene_list = [item for sublist in data_list_of_list for item in sublist]
df = pd.DataFrame(all_data)


# In[33]:


no_col = len(df.columns)
no_col


# In[34]:


selected_gene_list = []
read_file  = open ('McTwo/GDS3268.txt','r').read().splitlines()
for i in read_file:
    temp = df.iloc[int(i)-1,0]
    selected_gene_list.append(temp)


# In[35]:


print selected_gene_list


# In[36]:


df.iloc[:,0]


# In[37]:


my_df  = pd.DataFrame()
for i in range(len(selected_gene_list)):
    print i
    row = df.loc[df.iloc[:,0]== selected_gene_list[i], 2:(no_col-1)]
    row = np.array(row.values, dtype=np.float32)
    my_df  = my_df.append(pd.DataFrame(row))
    #my_df.append(my_df, ignore_index=True)


# In[38]:


my_df


# In[39]:


my_df.to_csv("significant_genes_GDS3268_Ge.txt", sep="\t", header=False, index=False)

