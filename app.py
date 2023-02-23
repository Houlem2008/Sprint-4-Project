#!/usr/bin/env python
# coding: utf-8

import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('moved_vehicles_us.csv')

# Overview of data

df.info()

df.head(10)

# Preprocessing data

df['date_posted'] = pd.to_datetime(df['date_posted'], format='%Y-%m-%d') # Converting dates to datetime data type
df.isna().sum() # Getting a count of missing values by column

# The `is_4wd` column appears to contain the value of `1.0` if the vehicle was listed to have four wheel drive, and a missing value if not. This will be confirmed to get the unique values, including missing from this column, and if there are only the two aforementioned values, we will replace missing values with `0` (zero) and convert them to integers to act as a Bulian true or false, 1 = true, 0 = false. This doesn't mean that all the vehicles listed with a 0 (zero) do not have four wheel drive, but that they were not advertised to have it.

df['is_4wd'].value_counts(dropna=False)

df['is_4wd'] = df['is_4wd'].fillna(0)
df = df.astype({'is_4wd':'int64'})
df['is_4wd'].value_counts(dropna=False)

makemodel = df["model"].str.split(" ", n = 1, expand = True)
df['make'] = makemodel[0]
df['model'] = makemodel[1]
df.rename(columns={'model_year':'year', 'paint_color':'color'}, inplace=True)
df = df[['price', 'year', 'make', 'model', 'condition', 'cylinders', 'fuel','odometer', 'transmission', 'type', 'color', 'is_4wd', 'date_posted', 'days_listed']]

# Streamlit coding

st.header('Exploratory Analysis of Auto Listings')
st.write('''
The goal of this exploratory analysis is to use the interactive displays provided to assess trends and/or patterns relating to the listing of automobiles posted to be sold.
''')
st.write('''
Default display of vehicles only includes those listed for 30 days or less. In order to see all listings, including those listed for more than 30 days, click the checkbox below.
''')
old_listings = st.checkbox('Show cars listed over 30 days')

# Checkbox to include vehicles posted for over 30 days
if not old_listings:
    df = df[df.days_listed<=30]


# histogram for price(y) based on year(x) (slider for year)

# Selectbox for histogram
hist_list = ['condition', 'fuel', 'transmission', 'type', 'is_4wd']
hist_select = st.selectbox('Filter for average price', hist_list)

# Slider for year, limits then slider
min_year, max_year = int(df['year'].min()), int(df['year'].max())

year_range = st.slider(
    'Choose years',
    value=(min_year, max_year), min_value=min_year, max_value=max_year )

year_act_range = list(range(year_range[0],year_range[1]+1))
year_df = df[(df.year.isin(list(year_act_range)))]

fig1 = px.histogram(year_df, x='year', y='price', histfunc='avg', color=hist_select)

fig1.update_layout(title='<b>Average Price by Year</b>')

st.plotly_chart(fig1)

fig1.show()

# scatterplot for odometer(y) based on price(x) (slider for price)

# Selectbox for scatterplot
scat_list = ['condition', 'fuel', 'transmission', 'type', 'is_4wd']
scat_select = st.selectbox('Filter for mileage by price', scat_list)

# Slider for price, limits then slider
min_price, max_price = int(df['price'].min()), int(df['price'].max())

price_range = st.slider(
    'Set price range',
    value=(min_price, max_price), min_value=min_price, max_value=max_price )

price_act_range = list(range(price_range[0],price_range[1]+1))
price_df = df[(df.price.isin(list(price_act_range)))]

fig2 = px.scatter(price_df, x='price', y='odometer', color=scat_select)

fig2.update_layout(title='<b>Mileage by Price (USD)</b>')

st.plotly_chart(fig2)

fig2.show()

# boxplot for odometer (y) based on cylinders (slider of cylinders)

# Selectbox for box chart
box_list = ['condition', 'fuel', 'transmission', 'type', 'is_4wd']
box_select = st.selectbox('Filter for mileage by cylinder count', box_list)

# Slider of cylinders, limits then slider
min_cyl, max_cyl = int(df['cylinders'].min()), int(df['cylinders'].max())

cyl_range = st.slider(
    'Specify number of cylinders',
    value=(min_cyl, max_cyl), min_value=min_cyl, max_value=max_cyl )

cyl_act_range = list(range(cyl_range[0],cyl_range[1]+1))
cyl_df = df[(df.cylinders.isin(cyl_act_range))]

fig3 = px.box(cyl_df, x='cylinders', y='odometer', color=box_select)

fig3.update_layout(title='<b>Distribution of Mileage by Cylinder Count</b>')

st.plotly_chart(fig3)

fig3.show()
