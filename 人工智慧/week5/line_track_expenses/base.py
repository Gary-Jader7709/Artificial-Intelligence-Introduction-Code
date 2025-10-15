"""========================================================
啟動教學（開發機）：
1) 安裝套件
   pip install flask line-bot-sdk

2) 設定環境變數（請用你的憑證）
   - macOS/Linux:
       export LINE_CHANNEL_ACCESS_TOKEN="你的token"
       export LINE_CHANNEL_SECRET="你的secret"
   - Windows (PowerShell):
       setx LINE_CHANNEL_ACCESS_TOKEN "你的token"
       setx LINE_CHANNEL_SECRET "你的secret"

3) 啟動本機伺服器
   python base.py

4) 用 ngrok 暴露 5000 連接埠（或等同工具）
   ngrok http 127.0.0.1:5000

5) 到 LINE Developers Console 設定 Webhook URL：
   https://<你的-ngrok-subdomain>.ngrok.io/

6) 在聊天視窗隨便傳文字，機器人會回聲相同內容
========================================================"""
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET")
if not ACCESS_TOKEN or not CHANNEL_SECRET:
    raise RuntimeError("Missing LINE credentials in environment variables")

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature', '')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))

if __name__ == "__main__":
    # 明確指定 host/port，便於 ngrok 轉發
    app.run(host="0.0.0.0", port=5000, debug=True)
