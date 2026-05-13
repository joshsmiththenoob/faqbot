""" 
Event handler is like "Core view" in the traditional MVC architecture

It receives the event dispatched by the main service then parse it 
and send it to the core service to operate bussiness logic.

"""
from apps.faq.service.follow_event_service import FollowEventService
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.messaging import (
    TextMessage,
    QuickReply,
    QuickReplyItem,
    MessageAction,
)
from apps.faq.handler.line_client import LineClient
from apps.faq.service.message_event_service import MessageEventService



class MessageEventHandler():
    def __init__(self):
        self.line_client = LineClient()
        self.message_event_service = MessageEventService()

    def handle(self, event: MessageEvent) -> None:
        reply_token = event.reply_token

        if not isinstance(event.message, TextMessageContent):
            support_message = self.message_event_service.reply_support_text()

            self.line_client.reply_message(
                reply_token=reply_token,
                messages=[support_message],
            )

            return
                

        user_text = event.message.text.strip()

        if not user_text:
            support_question_message = self.message_event_service.replay_support_text_question()

            self.line_client.reply_message(
                event.reply_token,
                support_question_message
            )
            return
        
        message_event_service.