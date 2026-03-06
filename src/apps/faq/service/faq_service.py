"""
The Service layer contains the business logic of the FAQ application. 
It processes data and finds similarity between client's question and the stored FAQs. A
Also, it handles the communication with the LINE Messaging API to send responses back to the user. 
"""

import os
from django.conf import settings
from linebot import LineBotApi, WebhookParser



class FAQService:
    def __init__(self, line_bot_api: LineBotApi, parser):
        self.line_bot_api = line_bot_api
        self.parser = parser
