""" 
Event handler is like "Core view" in the traditional MVC architecture

It receives the event dispatched by the main service then parse it 
and send it to the core service to operate bussiness logic.

"""
from linebot.v3.webhooks import FollowEvent, MessageEvent

from apps.faq.handler.line_client import LineClient
from apps.faq.service.follow_event_service import FollowEventService



class FollowEventHandler():
    def __init__(self):
        self.line_client = LineClient()
        self.follow_event_service = FollowEventService()

    def handle(self, event: FollowEvent) -> None:
        reply_token = event.reply_token

        # get user ID from event
        user_id = getattr(event.source, 'user_id', None)

        print(f"New follower user_id={user_id}")

        # send welcome message to user
        welcome_message = self.follow_event_service.build_welcome_message()


        self.line_client.reply_message(
            reply_token=reply_token,
            messages=[welcome_message],
        )