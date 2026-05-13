"""
Duty of handle FollowEvent from event handler,
FollowEvent: When LINEBOT get a new friend(client), it build welcome message for User throught Message API from this service!!
"""
from rapidfuzz import fuzz, process


from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import (
    TextMessage,
    QuickReply,
    QuickReplyItem,
    MessageAction,
)


from apps.faq.models import FAQ
from apps.faq.handler.line_client import LineClient

class MessageEventService:
    def __init__(self):
        self.line_client = LineClient()
        self.messaging_api = self.line_client.messaging_api


    def reply_support_text(self):
        support_text = (
        "目前先支援文字問題，請直接輸入您想查詢的內容。"
        )

        return TextMessage(text=support_text)
    

    def replay_support_text_question(self):
        support_question = (
            "請輸入想查詢的問題。"
        )
        return TextMessage(text=support_question)
    

    def find
