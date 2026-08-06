import os
import yaml
from src.fetchers.data_fetcher import DataFetcher
from src.processors.data_processor import DataProcessor
from src.summaries.summary_engine import SummaryEngine
from src.summaries.llm_commentator import LLMCommentator
from dotenv import load_dotenv

load_dotenv()

def main():
    print("🚀 開始每日自動化流程...")
    
    config_path = 'config/watchlist.yaml'
    raw_data_dir = 'data/raw'
    processed_data_dir = 'data/processed'
    report_dir = 'reports'
    os.makedirs(report_dir, exist_ok=True)
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # 1. 數據獲取
    print("📥 正在獲取最新數據...")
    fred_key = os.getenv('FRED_API_KEY')
    fetcher = DataFetcher(config_path, fred_api_key=fred_key)
    fetcher.run()

    # 2. 數據處理
    print("⚙️ 正在處理數據指標...")
    processor = DataProcessor(raw_data_dir, processed_data_dir)
    processor.process_market_data()
    processor.process_yield_data()

    # 3. 生成摘要與評述
    print("✍️ 正在生成市場評述...")
    engine = SummaryEngine(processed_data_dir, config)
    highlights = engine.get_market_highlights()
    
    rule_text = engine.generate_rule_based_text(highlights)
    
    commentator = LLMCommentator()
    llm_text = commentator.generate_commentary(highlights)

    # 4. 匯出報告
    report_path = os.path.join(report_dir, f"market_report_{highlights['date']}.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"# 📊 市場情報每日報告\n\n")
        f.write(rule_text)
        f.write("\n---\n")
        f.write(f"### 🤖 AI 深度評述\n\n")
        f.write(llm_text)
        f.write("\n\n---\n*本報告由市場情報平台自動生成*")

    print(f"✅ 報告已生成: {report_path}")

if __name__ == "__main__":
    main()
