import os
from openai import OpenAI
import json

class LLMCommentator:
    def __init__(self):
        # 使用 Manus 內置的 OpenAI 兼容環境
        self.client = OpenAI()

    def generate_commentary(self, highlights):
        """利用 LLM 生成市場評述"""
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
                model="gpt-4o",
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
