import streamlit as st
import pandas as pd
import os
import yaml

@st.cache_data
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), '../config/watchlist.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

@st.cache_data
def load_processed_data(filename):
    data_path = os.path.join(os.path.dirname(__file__), f'../data/processed/{filename}')
    if os.path.exists(data_path):
        return pd.read_parquet(data_path)
    return None

@st.cache_data
def load_raw_data(filename):
    data_path = os.path.join(os.path.dirname(__file__), f'../data/raw/{filename}')
    if os.path.exists(data_path):
        return pd.read_parquet(data_path)
    return None

def get_ticker_name(config, ticker):
    for category in ['indices', 'forex', 'commodities']:
        for item in config.get(category, []):
            if item['ticker'] == ticker:
                return item['name']
    return ticker
