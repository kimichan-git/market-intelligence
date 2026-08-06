import pandas as pd
import os

class YieldCurveAnalyzer:
    def __init__(self, processed_data_dir):
        self.data_path = os.path.join(processed_data_dir, 'yield_analysis.parquet')

    def get_latest_curve(self):
        """獲取最新的收益率曲線數據點"""
        df = pd.read_parquet(self.data_path)
        latest = df.iloc[-1]
        
        # 提取不同期限的收益率
        tenors = {
            '2Y': latest.get('DGS2'),
            '5Y': latest.get('DGS5'),
            '10Y': latest.get('DGS10'),
            '30Y': latest.get('DGS30')
        }
        return tenors

    def analyze_shape(self):
        """分析曲線形狀"""
        df = pd.read_parquet(self.data_path)
        latest = df.iloc[-1]
        spread_10y2y = latest.get('10Y-2Y')
        
        if spread_10y2y is None:
            return "Unknown"
            
        if spread_10y2y < 0:
            return "Inverted (倒掛)"
        elif spread_10y2y < 0.5:
            return "Flat (平坦)"
        else:
            return "Normal (正常/陡峭)"

    def get_historical_spreads(self):
        """獲取歷史利差數據"""
        df = pd.read_parquet(self.data_path)
        return df[['10Y-2Y']]

if __name__ == "__main__":
    analyzer = YieldCurveAnalyzer('data/processed')
    print(f"Latest Curve: {analyzer.get_latest_curve()}")
    print(f"Curve Shape: {analyzer.analyze_shape()}")
