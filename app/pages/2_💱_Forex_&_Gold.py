import streamlit as st
import pandas as pd
from utils import load_config, load_raw_data
from src.charts.chart_generator import ChartGenerator
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

st.set_page_config(page_title="外匯與黃金", layout="wide")

st.title("💱 外匯與黃金分析")

config = load_config()
market_df = load_raw_data('market_data.parquet')

if market_df is not None:
    # 合併外匯和商品
    assets = config['forex'] + config['commodities']
    tickers = [item['ticker'] for item in assets]
    
    selected_ticker = st.sidebar.selectbox(
        "選擇資產", 
        tickers, 
        format_func=lambda x: next(i['name'] for i in assets if i['ticker'] == x)
    )
    
    chart_gen = ChartGenerator()
    name = next(i['name'] for i in assets if i['ticker'] == selected_ticker)
    
    fig = chart_gen.plot_price_history(market_df, selected_ticker, name)
    st.plotly_chart(fig, use_container_width=True)
    
    # 展示數據表格
    if st.checkbox("顯示原始數據"):
        st.dataframe(market_df[[selected_ticker]].tail(10))
else:
    st.error("找不到數據。")
