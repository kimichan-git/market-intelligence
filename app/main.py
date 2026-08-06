import sys
from pathlib import Path

# Add the repository root and inner root to Python's search path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
INNER_DIR = Path(__file__).resolve().parent.parent
sys.path.extend([str(ROOT_DIR), str(INNER_DIR)])

# Existing imports follow below:
import streamlit as st
import pandas as pd
from utils import load_config, load_processed_data, load_raw_data, get_ticker_name
from src.analytics.yield_curve_analyzer import YieldCurveAnalyzer

import streamlit as st
import pandas as pd
from utils import load_config, load_processed_data, load_raw_data, get_ticker_name
from src.analytics.yield_curve_analyzer import YieldCurveAnalyzer
import sys
import os

# 確保可以導入 src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

st.set_page_config(page_title="市場情報平台", layout="wide")

# 自定義 CSS
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 市場情報概覽")
st.markdown("---")

# 加載數據
config = load_config()
market_df = load_raw_data('market_data.parquet')
returns_df = load_processed_data('returns.parquet')
yield_df = load_processed_data('yield_analysis.parquet')

if market_df is not None and returns_df is not None:
    # 1. 關鍵指標 (Top Metrics)
    st.subheader("🚀 核心市場指標")
    cols = st.columns(4)
    
    # 選取幾個代表性資產
    major_assets = ['^GSPC', '^IXIC', 'GC=F', 'EURUSD=X']
    asset_labels = {
        '^GSPC': "S&P 500",
        '^IXIC': "NASDAQ",
        'GC=F': "Gold",
        'EURUSD=X': "EUR/USD"
    }
    
    for i, ticker in enumerate(major_assets):
        if ticker in market_df.columns:
            last_price = market_df[ticker].iloc[-1]
            daily_change = returns_df[ticker].iloc[-1] * 100
            
            cols[i % 4].metric(
                label=asset_labels[ticker],
                value=f"{last_price:,.2f}",
                delta=f"{daily_change:.2f}%"
            )

    st.markdown("---")

    # 2. 宏觀摘要
    st.subheader("🌐 宏觀環境摘要")
    m_col1, m_col2 = st.columns(2)
    
    with m_col1:
        st.info("💡 **市場情緒**")
        vix_val = market_df.get('^VIX') # 假設有 VIX
        if vix_val is not None:
            st.write(f"VIX 指數: {vix_val.iloc[-1]:.2f}")
        else:
            st.write("目前市場波動率處於正常區間。")
            
    with m_col2:
        st.info("📈 **收益率曲線**")
        analyzer = YieldCurveAnalyzer(os.path.join(os.path.dirname(__file__), '../data/processed'))
        shape = analyzer.analyze_shape()
        st.write(f"當前形狀: **{shape}**")
        if '10Y-2Y' in yield_df.columns:
            st.write(f"10Y-2Y 利差: {yield_df['10Y-2Y'].iloc[-1]:.2f}%")

else:
    st.warning("請先執行數據採集腳本以生成數據。")
    st.code("python run_ingestion.py\npython run_week2.py")
