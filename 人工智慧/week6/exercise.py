import os
import re
from openai import OpenAI
from dotenv import load_dotenv

# 自動讀取 .env 的 API 金鑰
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not set. 請在 .env 中設定你的金鑰")

client = OpenAI(api_key=api_key)

# 自動抓同資料夾的 prompt.txt
base_dir = os.path.dirname(__file__)
prompt_path = os.path.join(base_dir, "prompt.txt")

with open(prompt_path, "r", encoding="utf-8") as f:
    prompt = f.read().strip()

def validate_and_normalize(s: str) -> str:
    """檢查模型輸出格式是否正確"""
    s = s.strip()
    if s == "error":
        return "error"
    match = re.fullmatch(r"([^\s,][^,]*)\s*,\s*(0|[1-9]\d*)", s)
    if not match:
        return "error"
    item = match.group(1).strip()
    amount = match.group(2)
    return f"{item},{amount}"

print("🧾 記帳助理已啟動！（輸入 exit 可結束）")
print("請輸入消費內容，例如：『我今天午餐吃牛肉麵花了130元』")

while True:
    user_input = input("\n你說：").strip()
    if user_input.lower() in {"exit", "quit"}:
        print("\n👋 程式結束，謝謝使用！")
        break

    # 呼叫模型
    try:
        resp = client.responses.create(
    model="gpt-4o-mini",   # 更強、更準
    instructions=prompt,
    input=user_input,
    max_output_tokens=100
)


        model_text = resp.output_text.strip()
        result = validate_and_normalize(model_text)

        print(f"🧠 模型輸出：{model_text}")
        print(f"✅ 檢查結果：{result}")

    except Exception as e:
        print(f"⚠️ 錯誤：{e}")

