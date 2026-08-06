import streamlit as st
import pandas as pd
from utils import load_config, load_raw_data, load_processed_data
from src.charts.chart_generator import ChartGenerator
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

st.set_page_config(page_title="指數分析", layout="wide")

st.title("📈 股票指數分析")

config = load_config()
market_df = load_raw_data('market_data.parquet')
returns_df = load_processed_data('returns.parquet')

if market_df is not None:
    # 側邊欄過濾器
    indices = [item['ticker'] for item in config['indices']]
    selected_ticker = st.sidebar.selectbox("選擇指數", indices, format_func=lambda x: next(i['name'] for i in config['indices'] if i['ticker'] == x))
    
    date_range = st.sidebar.date_input("選擇日期範圍", [market_df.index[0], market_df.index[-1]])
    
    # 過濾數據
    filtered_df = market_df.loc[str(date_range[0]):str(date_range[1])]
    
    # 顯示圖表
    chart_gen = ChartGenerator()
    name = next(i['name'] for i in config['indices'] if i['ticker'] == selected_ticker)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        fig = chart_gen.plot_price_history(filtered_df, selected_ticker, name)
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.subheader("統計指標")
        last_price = filtered_df[selected_ticker].iloc[-1]
        period_return = (filtered_df[selected_ticker].iloc[-1] / filtered_df[selected_ticker].iloc[0] - 1) * 100
        
        st.metric("最新價格", f"{last_price:,.2f}")
        st.metric("區間回報", f"{period_return:.2f}%")
        
        if returns_df is not None:
            vol = returns_df[selected_ticker].std() * (252**0.5) * 100
            st.metric("年化波動率", f"{vol:.2f}%")
else:
    st.error("找不到數據。")
