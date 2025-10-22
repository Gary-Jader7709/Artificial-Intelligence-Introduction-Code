"""
讀取 prompt.txt 當成角色指令，示範 instructions 用法
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not set.")

client = OpenAI(api_key=api_key)

# 讀取 txt 檔內容（修正成 prompt.txt）
with open("prompt.txt", "r", encoding="utf-8") as f:
    prompt = f.read().strip()

# 呼叫 GPT 模型
response = client.responses.create(
    model="gpt-5-nano",
    instructions=prompt,        # 定義角色或各種回應的方式
    input="我昨天午餐花了120元"
)

# 輸出結果（理想：午餐,120）
print(response.output_text)
