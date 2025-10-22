"""
簡單測試：確認 API 連線與 Responses API 可用
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not set.")

client = OpenAI(api_key=api_key)

resp = client.responses.create(
  model="gpt-5-nano",
  input="hello"
)

print(resp.output_text)
