"""
The Service layer contains the business logic of the FAQ application. 
It processes data and finds similarity between client's question and the stored FAQs. A
Also, it handles the communication with the LINE Messaging API to send responses back to the user. 
"""

import os
from django.conf import settings
from apps.faq.handler.line_client import LineClient



class LineWebhookService():
    def __init__(self):
        self.line_handler = LineClient()
        

    def handle_webhook(self, body: str, signature: str):

        print("Signature:", signature, "\n", "Type:", type(signature), "\n", "Body:", body, "\n", "Type:", type(body))
        
        # 這裡可以調用 LineHandler 的方法來處理 webhook 邏輯
        linebot_api = self.line_handler.line_bot_api
        parser = self.line_handler.webhook_parser

        
        try:
            events = parser.parse(body, signature)
        except Invalid
        
        