import streamlit as st
import glob
import pandas as pd

@st.cache_data
def combine_data(path):
    dfs = [pd.read_csv(file) for file in glob.glob(path)]
    combined_df = pd.concat(dfs, ignore_index=True)
    return combined_df


@st.cache_data
def process_data(df):

    df = df.dropna(how='all')


    df = df[df['Order ID'] != 'Order ID']
    

    df['Order Date'] = df['Order Date'].str.replace('/', '-')
    df['Quantity Ordered'] = pd.to_numeric(df['Quantity Ordered'])
    df['Price Each'] = pd.to_numeric(df['Price Each'])
    df['Order ID'] = pd.to_numeric(df['Order ID'])
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed',errors='coerce')


    df.rename(columns={'Order Date': 'Order DateTime'}, inplace=True)


    df['Date'] = df['Order DateTime'].dt.date
    df['Month'] = df['Order DateTime'].dt.month
    df['Weekday'] = df['Order DateTime'].dt.weekday
    df['MonthDay'] = df['Order DateTime'].dt.day
    df['Hour'] = df['Order DateTime'].dt.hour
    df['Minute'] = df['Order DateTime'].dt.minute
    df['Sales'] = df['Quantity Ordered'] * df['Price Each']

    def get_city_state(address):
        city = address.split(', ')[1]
        state = address.split(', ')[2].split(' ')[0]
        return f"{city} {state}"
    df['City State'] = df['Purchase Address'].apply(get_city_state)

    return df

