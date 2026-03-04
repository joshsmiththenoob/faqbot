import os
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction
from .models import FAQ
from rapidfuzz import fuzz, process



def check_channel_config(self) -> None:
    """
    Check if the LINE channel configuration is set properly.

    Raises:
        ValueError: If the LINE channel secret or access token is not set.
    """
    if not settings.CHANNEL_SECRET:
        raise ValueError("LINE_CHANNEL_SECRET is not set.")
    if not settings.CHANNEL_ACCESS_TOKEN:
        raise ValueError("LINE_CHANNEL_ACCESS_TOKEN is not set.")
        
check_channel_config()
line_bot_api = LineBotApi(settings.CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.CHANNEL_SECRET)





# 在你的 views 回覆 FAQ 前
def _send_long_text(line_bot_api, reply_token, text, max_len=1800):
    parts = []
    cur = []
    cur_len = 0
    for line in text.splitlines(True):  # 保留換行
        if cur_len + len(line) > max_len:
            parts.append("".join(cur))
            cur = [line]; cur_len = len(line)
        else:
            cur.append(line)
            cur_len += len(line)
    if cur: 
        parts.append("".join(cur))
    msgs = [TextSendMessage(text=p) for p in parts]
    line_bot_api.reply_message(reply_token, msgs if len(msgs) > 1 else msgs[0])



def _match(user_text: str, faqs):
    # ① alias/包含比對
    t = user_text.strip()
    for f in faqs:
        for phr in [f.question, *f.aliases]:
            if phr and (phr == t or phr in t or t in phr):
                return f, []

    # ② 模糊比對（取前 3 名）
    universe, idx_map = [], []
    for i, f in enumerate(faqs):
        for phr in [f.question, *f.aliases]:
            if phr: 
                universe.append(phr) 
                idx_map.append(i)

    ranked = process.extract(t, universe, scorer=fuzz.WRatio, limit=5)
    print(ranked)
    scores = {}
    for phr, sc, uidx in ranked:
        f = faqs[idx_map[uidx]]
        scores[f] = max(scores.get(f, 0), sc)

    top = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:3]
    if top and top[0][1] >= 90:
        return top[0][0], []
    sugg = [f.question for f, sc in top if sc >= 60]
    return None, sugg

@csrf_exempt
def callback(request):
    # print("SECRET head:", (settings.CHANNEL_SECRET or "")[:6], "len:", len(settings.CHANNEL_SECRET or "0"))
    # print("TOKEN head:", (settings.CHANNEL_ACCESS_TOKEN or "")[:6], "len:", len(settings.CHANNEL_ACCESS_TOKEN or "0"))
    if not settings.CHANNEL_SECRET:
        raise RuntimeError("LINE_CHANNEL_SECRET is missing. Check .env")

    # 只接受 POST；其餘直接回 200
    if request.method != "POST":
        return HttpResponse("ok", status=200)

    signature = request.headers.get("X-Line-Signature", "")
    body = request.body.decode("utf-8") if request.body else ""
    # LINE 的 Verify 可能丟空 body：直接 200
    if not body.strip():
        return JsonResponse({"status": "ok-empty"}, status=200)

    # 沒簽章也別報錯給 LINE（僅記錄）
    if not signature:
        return JsonResponse({"status": "missing-signature"}, status=200)

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        # 簽章不對：回 200，避免 Verify 失敗；同時方便你在 console 看到成功
        print("簽章不對")
        return JsonResponse({"status": "invalid-signature-ignored"}, status=200)
    except Exception as e:
        # 其他解析錯誤也先回 200
        print("parse error:", e)
        return JsonResponse({"status": "parse-error-ignored"}, status=200)

    faqs = list(FAQ.objects.filter(enabled=True))
    print(faqs)
    # 你的比對邏輯（略）——保留原本 reply 邏輯
    for ev in events:
        if isinstance(ev, MessageEvent) and isinstance(ev.message, TextMessage):
            text = ev.message.text.strip()
            faq, suggestions = _match(text, faqs)
            if faq:
                line_bot_api.reply_message(ev.reply_token, TextSendMessage(text=faq.answer))
            elif suggestions:
                buttons = [QuickReplyButton(action=MessageAction(label=q[:20], text=q)) for q in suggestions]
                msg = TextSendMessage(text="您想問的是以下其中一題嗎？", quick_reply=QuickReply(items=buttons))
                line_bot_api.reply_message(ev.reply_token, msg)
            else:
                line_bot_api.reply_message(ev.reply_token, TextSendMessage(text="抱歉我還不確定，請換個說法或點選建議問題 🙏"))

    return JsonResponse({"status": "ok"}, status=200)



