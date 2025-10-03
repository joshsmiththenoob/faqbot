# app.py
import os
import time
import json
import uvicorn
from fastapi import FastAPI, Request, Header, HTTPException, BackgroundTasks
from logging.handlers import TimedRotatingFileHandler
from logging import getLogger, Formatter, INFO
from pydantic import BaseModel
from linebot import LineBotApi, WebhookParser
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv

load_dotenv()  # 讀 .env

CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if not CHANNEL_SECRET or not CHANNEL_ACCESS_TOKEN:
    raise RuntimeError(
        "Missing LINE credentials. Set LINE_CHANNEL_SECRET & LINE_CHANNEL_ACCESS_TOKEN "
        "via environment variables or a .env file."
    )



app = FastAPI(debug= True)
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(CHANNEL_SECRET)

class LineWebhookBody(BaseModel):
    destination: str | None = None
    events: list[dict]

@app.post("/callback")
async def callback(
    request: Request,
    background_tasks: BackgroundTasks,
    x_line_signature: str = Header(None)
):
    body_bytes = await request.body()
    body_text = body_bytes.decode("utf-8")

    # 只有在 header 存在的時候才驗簽
    if x_line_signature:
        try:
            events = parser.parse(body_text, x_line_signature)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid signature")
    else:
        # 開發測試：手動組一個最簡單事件（或直接 json.loads(body_text)）
        raw = json.loads(body_text or '{"events": []}')
        # 若你本來依賴 parser 產物，就簡單處理 raw['events']

    # 快速回 200，實際處理丟背景（避免超時）
    def handle_events():
        for event in events:
            if isinstance(event, MessageEvent) and isinstance(event.message, TextMessage):
                reply = TextSendMessage(text=f"你說：{event.message.text}")
                line_bot_api.reply_message(event.reply_token, reply)
                root.info(event.message.text)

    background_tasks.add_task(handle_events)
    return {"status": "ok"}


if __name__ == "__main__":
    logPath = os.getcwd() + "/app_logs/linebot"

    if not os.path.isdir(logPath):
        os.makedirs(logPath)

    root = getLogger()
    if len(root.handlers) == 0:
        fileName = logPath + "/log_" + time.strftime("%Y%m%d")
        fileHandler = TimedRotatingFileHandler(
            fileName, when="midnight", backupCount=180
        )
        fileHandler.setFormatter(
            Formatter(
                "[%(asctime)s] linebot %(levelname)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        )
        root.addHandler(fileHandler)
        root.setLevel(INFO)

    uvicorn.run(app= "app:app", host="0.0.0.0", port=8081, reload= True)