import yfinance as yf
import pandas as pd
from fredapi import Fred
import os
import yaml
from datetime import datetime, timedelta
from src.utils.logger import setup_logger

logger = setup_logger("DataFetcher")

class DataFetcher:
    def __init__(self, config_path, fred_api_key=None):
        with open(config_path, 'r') as file:
            self.config = yaml.safe_load(file)
        
        self.fred = Fred(api_key=fred_api_key) if fred_api_key else None
        self.raw_data_path = os.path.join(os.path.dirname(__file__), '../../data/raw')
        os.makedirs(self.raw_data_path, exist_ok=True)

    def fetch_yfinance_data(self, tickers, period="2y", interval="1d"):
        """獲取 yfinance 數據 (指數、外匯、黃金)"""
        try:
            logger.info(f"Fetching yfinance data for: {tickers}")
            data = yf.download(tickers, period=period, interval=interval)
            if data.empty:
                logger.warning("yfinance returned empty dataframe")
                return pd.DataFrame()
                
            if len(tickers) > 1:
                close_data = data['Close']
            else:
                close_data = data['Close'].to_frame()
                close_data.columns = tickers
            return close_data
        except Exception as e:
            logger.error(f"Error fetching yfinance data: {str(e)}")
            return pd.DataFrame()

    def fetch_fred_data(self, series_ids, start_date=None):
        """獲取 FRED 數據 (收益率曲線)"""
        if not self.fred:
            print("Warning: FRED API key not provided. Skipping FRED data.")
            return pd.DataFrame()
        
        if not start_date:
            start_date = (datetime.now() - timedelta(days=365*2)).strftime('%Y-%m-%d')
            
        fred_df = pd.DataFrame()
        for s_id in series_ids:
            print(f"Fetching FRED series: {s_id}")
            s_data = self.fred.get_series(s_id, observation_start=start_date)
            fred_df[s_id] = s_data
            
        return fred_df

    def run(self):
        """執行完整的數據採集流程"""
        # 1. 處理 yfinance 資產
        yf_tickers = []
        for category in ['indices', 'forex', 'commodities']:
            if category in self.config:
                yf_tickers.extend([item['ticker'] for item in self.config[category]])
        
        if yf_tickers:
            yf_data = self.fetch_yfinance_data(yf_tickers)
            yf_data.to_parquet(os.path.join(self.raw_data_path, 'market_data.parquet'))
            print(f"Saved yfinance data to market_data.parquet")

        # 2. 處理 FRED 資產
        if 'yield_curve' in self.config and self.fred:
            fred_ids = [item['series_id'] for item in self.config['yield_curve']]
            fred_data = self.fetch_fred_data(fred_ids)
            fred_data.to_parquet(os.path.join(self.raw_data_path, 'yield_data.parquet'))
            print(f"Saved FRED data to yield_data.parquet")

if __name__ == "__main__":
    # 測試代碼 (不帶 API Key)
    fetcher = DataFetcher('config/watchlist.yaml')
    # 這裡僅測試 yfinance，因為 FRED 需要 API Key
    yf_tickers = [item['ticker'] for item in fetcher.config['indices']]
    data = fetcher.fetch_yfinance_data(yf_tickers, period="1mo")
    print(data.head())
