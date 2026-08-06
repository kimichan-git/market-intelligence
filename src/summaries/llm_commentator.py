import os
import json
from dotenv import load_dotenv

# 1. 自動載入本地 .env 檔案
load_dotenv()

class LLMCommentator:
    def __init__(self):
        # 2. 優先從 Streamlit Secrets 讀取，讀不到再讀系統/環境變數 os.getenv
        self.xai_key = self._get_secret('XAI_API_KEY')
        self.openai_key = self._get_secret('OPENAI_API_KEY')
        
        self.client = None
        self.model = "grok-4.3" # 預設使用 xAI 的模型
        
        if self.xai_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(
                    api_key=self.xai_key,
                    base_url="https://api.x.ai/v1",
                )
                print("Using xAI (Grok) for commentary.")
            except ImportError:
                print("Warning: 'openai' package not installed.")
        elif self.openai_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.openai_key)
                self.model = "gpt-4o"
                print("Using OpenAI for commentary.")
            except ImportError:
                pass

    def _get_secret(self, key_name):
        """兼容 Streamlit Cloud Secrets 與標準環境變數"""
        # 先嘗試 Streamlit Secrets
        try:
            import streamlit as st
            if key_name in st.secrets:
                return st.secrets[key_name]
        except Exception:
            pass
        # 再嘗試系統環境變數 (.env 或 export)
        return os.getenv(key_name)

    def generate_commentary(self, highlights):
        """利用 LLM 生成市場評述"""
        if not self.client:
            return "AI 評述已跳過：未配置 XAI_API_KEY 或 OPENAI_API_KEY，或未安裝 'openai' 套件。"

        prompt = f"""
        你是一位資深的全球市場策略師。請根據以下當日市場數據亮點，撰寫一段專業、簡潔且具備洞察力的市場評述（約 200 字）。
        
        數據亮點：
        - 日期：{highlights['date']}
        - 表現最好：{highlights['top_performer']['name']} ({highlights['top_performer']['change']})
        - 表現最差：{highlights['worst_performer']['name']} ({highlights['worst_performer']['change']})
        - 10Y-2Y 國債利差：{highlights['yield_spread_10y2y']} (今日變動: {highlights['yield_spread_change']})
        
        請分析這些變化背後的潛在邏輯（例如：風險偏好轉移、通脹預期或貨幣政策影響），並以專業的口吻輸出。
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位專業的金融分析師。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            if response and response.choices:
                return response.choices[0].message.content
            return "LLM 評述生成失敗: 未收到有效回應"
        except Exception as e:
            return f"LLM 評述生成失敗: {str(e)}"
