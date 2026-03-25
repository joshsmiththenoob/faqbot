"""
The Service layer contains the business logic of the FAQ application. 
It processes data and finds similarity between client's question and the stored FAQs. A
Also, it handles the communication with the LINE Messaging API to send responses back to the user. 
"""

import os
from django.conf import settings
from faq.handler.line_handler import LineHandler



class FAQService:
    def __init__(self):
        self.line_handler = LineHandler()
        

    def handle_webhook(self, request):
        # 在這裡處理 LINE Webhook 的回調邏輯
        signature = request.headers.get("X-Line-Signature", "")
        body = request.body.decode("utf-8") if (request.body) else ""

        print("Signature:", signature, "\n", "Type:", type(signature), "\n", "Body:", body, "\n", "Type:", type(body))
        
        # 這裡可以調用 LineHandler 的方法來處理 webhook 邏輯
        linebot_api = self.line_handler.line_bot_api
        parser = self.line_handler.webhook_parser

        
        try:
            events = parser.parse(body, signature)
        except Invalid
        
        