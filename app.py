#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import plotly.express as px


# #### What we need to include in the app: ####
# - at least one `st.header` with text
# - at least one `plotly-express` histogram using `[st.write][https://docs.streamlit.io/library/api-reference/write-magic/st.write][st.plotly_chart](https://docs.streamlit.io/library/api-reference/charts/st.plotly_chart)`
# - at least one `plotly-express` scatterplot using `[st.write][https://docs.streamlit.io/library/api-reference/write-magic/st.write][st.plotly_chart](https://docs.streamlit.io/library/api-reference/charts/st.plotly_chart)`
# - at least one checkbox that uses `[st.checkbox](https://docs.streamlit.io.library/api-reference/widgets/st.checkbox)` that changes the behavior of any of the above components

# In[2]:


df = pd.read_csv('moved_vehicles_us.csv')


# ### Overview of data

# In[3]:


df.info()


# In[4]:


df.head(10)


# ### Preprocessing data

# In[5]:


df['date_posted'] = pd.to_datetime(df['date_posted'], format='%Y-%m-%d') # Converting dates to datetime data type
df.isna().sum() # Getting a count of missing values by column


# The `is_4wd` column appears to contain the value of `1.0` if the vehicle was listed to have four wheel drive, and a missing value if not. This will be confirmed to get the unique values, including missing from this column, and if there are only the two aforementioned values, we will replace missing values with `0` (zero) and convert them to integers to act as a Bulian true or false, 1 = true, 0 = false. This doesn't mean that all the vehicles listed with a 0 (zero) do not have four wheel drive, but that they were not advertised to have it.

# In[6]:


df['is_4wd'].value_counts(dropna=False)


# In[7]:


df['is_4wd'] = df['is_4wd'].fillna(0)
df = df.astype({'is_4wd':'int64'})
df['is_4wd'].value_counts(dropna=False)


# In[8]:


makemodel = df["model"].str.split(" ", n = 1, expand = True)
df['make'] = makemodel[0]
df['model'] = makemodel[1]
df.rename(columns={'model_year':'year', 'paint_color':'color'}, inplace=True)
df = df[['price', 'year', 'make', 'model', 'condition', 'cylinders', 'fuel','odometer', 'transmission', 'type', 'color', 'is_4wd', 'date_posted', 'days_listed']]


# In[9]:


df


# ### Streamlit coding

# In[10]:


st.header('TITLE OF PROJECT')
st.write('''
Instruction on filters
''')
old_listings = st.checkbox('Show cars listed over 30 days')


# In[11]:


# Checkbox to include vehicles posted for over 30 days
if not old_listings:
    df = df[df.days_listed<=30]


# In[12]:


# Filter for different body types
body_type = df['type'].unique()
type_choice = st.selectbox('Select body type:', body_type)


# ##### histogram for price(y) based on year(x) (slider for year)

# In[13]:


# Slider for year, limits then slider
min_year, max_year = int(df['year'].min()), int(df['year'].max())

year_range = st.slider(
    'Choose years',
    value=(min_year, max_year), min_value=min_year, max_value=max_year )


# In[14]:


year_act_range = list(range(year_range[0],year_range[1]+1))
year_df = df[(df.type == type_choice) & (df.year.isin(list(year_act_range)))]


# In[15]:


fig1 = px.histogram(year_df, x='year', y='price', histfunc='avg', color='type')

fig1.update_layout(title='<b>Average Price by Year</b>')

st.plotly_chart(fig1)


# In[16]:


fig1.show()


# ##### scatterplot for odometer(y) based on price(x) (slider for price)

# In[17]:


# Slider for price, limits then slider
min_price, max_price = int(df['price'].min()), int(df['price'].max())

price_range = st.slider(
    'Set price range',
    value=(min_price, max_price), min_value=min_price, max_value=max_price )


# In[18]:


price_act_range = list(range(price_range[0],price_range[1]+1))
price_df = df[(df.type == type_choice) & (df.price.isin(list(price_act_range)))]


# In[19]:


fig2 = px.scatter(price_df, x='price', y='odometer', color='type')

fig2.update_layout(title='<b>Mileage by Price (USD)</b>')

st.plotly_chart(fig2)


# In[20]:


fig2.show()


# ##### boxplot for odometer (y) based on cylinders (slider of cylinders)

# In[21]:


# Slider of cylinders, limits then slider
min_cyl, max_cyl = int(df['cylinders'].min()), int(df['cylinders'].max())

cyl_range = st.slider(
    'Specify number of cylinders',
    value=(min_cyl, max_cyl), min_value=min_cyl, max_value=max_cyl )


# In[22]:


cyl_act_range = list(range(cyl_range[0],cyl_range[1]+1))
cyl_df = df[(df.type == type_choice) & (df.cylinders.isin(cyl_act_range))]


# In[23]:


fig3 = px.box(cyl_df, x='cylinders', y='odometer', color='type')

fig3.update_layout(title='<b>Distribution of Mileage by Cylinder Count</b>')

st.plotly_chart(fig3)


# In[24]:


fig3.show()


# In[ ]:




