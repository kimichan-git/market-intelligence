from src.processors.data_processor import DataProcessor
from src.analytics.yield_curve_analyzer import YieldCurveAnalyzer
from src.charts.chart_generator import ChartGenerator
import pandas as pd
import os

def main():
    print("--- Starting Week 2 Processing ---")
    
    # 1. 數據處理
    processor = DataProcessor('data/raw', 'data/processed')
    market_df, returns = processor.process_market_data()
    yield_df = processor.process_yield_data()
    
    # 2. 金融分析
    analyzer = YieldCurveAnalyzer('data/processed')
    latest_curve = analyzer.get_latest_curve()
    shape = analyzer.analyze_shape()
    
    print(f"\n最新收益率曲線: {latest_curve}")
    print(f"當前曲線形狀: {shape}")
    
    # 3. 生成圖表示例 (這裡僅演示邏輯，實際圖表會在 Streamlit 中顯示)
    # chart_gen = ChartGenerator()
    # fig = chart_gen.plot_yield_curve(latest_curve)
    # fig.show() # 在 sandbox 中無法直接顯示，但代碼已就緒
    
    print("\n--- Week 2 Completed Successfully ---")

if __name__ == "__main__":
    main()
