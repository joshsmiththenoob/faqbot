"""
Duty

1. parses webhook events from LINE Platform
2. dispatches each event to the corresponding event handler.
"""

import os
from django.conf import settings
from linebot.v3.webhooks import FollowEvent, MessageEvent
from apps.faq.handler.line_client import LineClient
from apps.faq.handler.event_handler.follow_event_handler import FollowEventHandler
from apps.faq.handler.event_handler.message_event_handler import MessageEventHandler



class LineWebhookDispatcher():
    def __init__(self):
        self.line_client = LineClient()
        

    def handle_webhook(self, body: str, signature: str) -> None:

        print("Signature:", signature, "\n", "Type:", type(signature), "\n", "Body:", body, "\n", "Type:", type(body))
        
        # Get parser from LineClient to handle the webhook request
        parser = self.line_client.webhook_parser

        
        # Get events by parsing the request body and signature
        events = parser.parse(body, signature)

        # Dispatch each event and handle it accordingly
        # Example: if there's a MesssageEvent, we can delegate the FAQService to handle the message etc.
        for event in events:
            self.dispatch(event)
        
        
    def dispatch(self, event) -> None:
        if isinstance(event, FollowEvent):
            FollowEventHandler().handle(event)

        elif isinstance(event, MessageEvent):
            MessageEventHandler().handle(event)
