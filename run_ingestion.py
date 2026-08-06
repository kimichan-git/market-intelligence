from src.fetchers.data_fetcher import DataFetcher
import os
from dotenv import load_dotenv

# 加載環境變量 (用於 FRED API KEY)
load_dotenv()

def main():
    config_path = 'config/watchlist.yaml'
    fred_api_key = os.getenv('FRED_API_KEY')
    
    print("--- Starting Market Data Ingestion ---")
    fetcher = DataFetcher(config_path, fred_api_key=fred_api_key)
    
    # 執行採集
    fetcher.run()
    
    print("--- Ingestion Completed ---")
    
    # 檢查結果
    raw_path = 'data/raw'
    files = os.listdir(raw_path)
    print(f"Files in {raw_path}: {files}")

if __name__ == "__main__":
    main()
