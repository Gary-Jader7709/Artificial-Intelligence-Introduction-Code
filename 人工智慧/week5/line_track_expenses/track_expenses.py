# ============================================================
# 第五週 LINE 記帳功能開發 - 俄文組版本
# ============================================================
# 使用教學：
# 1. pip install flask line-bot-sdk
# 2. 執行：python track_expenses.py
# 3. 使用 ngrok 網址：
#    https://nonserious-lorrine-directable.ngrok-free.dev/
#    將此網址填入 LINE Developers Console 的 Webhook URL
# ============================================================

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from datetime import datetime, timedelta
import csv, os, re

app = Flask(__name__)

# --- 你的 Channel 資訊（直接填入） ---
access_token = 'hc493FziAyddUq3Dl2JYLnIFlKrvi9d5JVMQsse3+9lS06MWumZ8W/fMP8gYlArwfjFNqRlBJOys3xJKIRMaaIqXTCpxIBWdVAtKc4yh/9nY4Ujz/Ix7mFFX1adRCCDAMQ65tTLgv7d3I0scjagWyAdB04t89/1O/w1cDnyilFU='
secret = '848851fec426647aa05a383dd85f5840'
webhook_url = 'https://nonserious-lorrine-directable.ngrok-free.dev/'  # 給 LINE Developers 設定 Webhook

line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(secret)

csv_path = "records.csv"
if not os.path.exists(csv_path):
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "item", "amount", "user_id"])


def save_record(item, amount, user_id):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(csv_path, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([now, item, amount, user_id])


def read_user_records(user_id):
    records = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["user_id"] == user_id:
                time = datetime.strptime(row["time"], "%Y-%m-%d %H:%M:%S")
                records.append({
                    "time": time,
                    "item": row["item"],
                    "amount": float(row["amount"])
                })
    return records


def sum_period(records, start, end):
    return sum(r["amount"] for r in records if start <= r["time"] < end)


@app.route("/", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    text = event.message.text.strip()
    reply = process_message(text, user_id)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))


def process_message(text, user_id):
    if text in ["說明", "help", "？", "?"]:
        return ("📒 記帳機器人使用說明\n"
                "➤ 新增記帳：午餐 120\n"
                "➤ 今日合計：今天\n"
                "➤ 本週合計：本週\n"
                "➤ 本月合計：本月\n"
                "➤ 列出紀錄：列表\n"
                "➤ 重置紀錄：重置")

    # 重置紀錄
    if text == "重置":
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = list(csv.DictReader(f))
        remain = [r for r in reader if r["user_id"] != user_id]
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["time", "item", "amount", "user_id"])
            writer.writeheader()
            writer.writerows(remain)
        return "✅ 已清空你的紀錄"

    # 查詢合計
    records = read_user_records(user_id)
    now = datetime.now()

    if text == "今天":
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        total = sum_period(records, start, end)
        return f"📅 今日合計：{total:.0f} 元"

    if text == "本週":
        start = now - timedelta(days=now.weekday())
        start = start.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=7)
        total = sum_period(records, start, end)
        return f"🗓️ 本週合計：{total:.0f} 元"

    if text == "本月":
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end = start.replace(month=start.month + 1 if start.month < 12 else 1)
        total = sum_period(records, start, end)
        return f"🗓️ 本月合計：{total:.0f} 元"

    if text.startswith("列表"):
        sorted_r = sorted(records, key=lambda r: r["time"], reverse=True)[:10]
        if not sorted_r:
            return "目前沒有紀錄喔～"
        lines = ["🧾 最近紀錄："]
        for r in sorted_r:
            lines.append(f"{r['time'].strftime('%m/%d %H:%M')} {r['item']} {r['amount']:.0f}")
        return "\n".join(lines)

    # 新增記帳
    match = re.search(r"(.+)\s+(\d+)", text)
    if match:
        item = match.group(1)
        amount = float(match.group(2))
        save_record(item, amount, user_id)
        return f"✅ 已記錄 {item} {amount:.0f} 元\n可輸入「今天 / 本週 / 本月」查看統計"
    return "指令不明，輸入「說明」查看使用方式。"


if __name__ == "__main__":
    print("伺服器啟動中...")
    print(f"Webhook URL: {webhook_url}")
    app.run(host="0.0.0.0", port=5000)
