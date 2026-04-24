""" 
Event handler is like "Core view" in the traditional MVC architecture

It receives the event dispatched by the main service then parse it 
and send it to the core service to operate bussiness logic.

"""
from linebot.v3.webhooks import FollowEvent



class FollowEventHandler():
    def __init__(self):
        pass

    def handle(self, event: FollowEvent) -> None:
        reply_token = event.reply_token

        # get user ID from event
        user_id = getattr(event.source, 'user_id', None)

        print(f"New follower user_id={user_id}")

        welcome_text = """
            您好，歡迎使用主力農家問題LINE Bot。 \n
            您可以直接輸入問題，例如: 農業保險、給付標準。\n
            我們會盡力為您提供相關資訊和協助。 \n
        """

        # send welcome message to user
        s