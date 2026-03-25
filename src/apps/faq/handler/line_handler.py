from django.conf import settings
from linebot.v3.messaging import(
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    QuickReply,
    QuickReplyItem
)

from linebot.v3 import (
    WebhookParser
)

class LineHandler():
    def __init__(self):
        self.__check_channel_config()

    def __check_channel_config(self) -> None:
        """
        Check if the LINE channel configuration is set properly.

        Raises:
            ValueError: If the LINE channel secret or access token is not set.
        """
        if not settings.CHANNEL_SECRET:
            raise ValueError("LINE_CHANNEL_SECRET is not set.")
        if not settings.CHANNEL_ACCESS_TOKEN:
            raise ValueError("LINE_CHANNEL_ACCESS_TOKEN is not set.")
        

    @property
    def line_bot_api(self):
        return MessagingApi(settings.CHANNEL_ACCESS_TOKEN)
    
    @property
    def webhook_parser(self):
        return WebhookParser(settings.CHANNEL_SECRET)
    


            


# def check_channel_config() -> None:
#     """
#     Check if the LINE channel configuration is set properly.

#     Raises:
#         ValueError: If the LINE channel secret or access token is not set.
#     """
#     if not settings.CHANNEL_SECRET:
#         raise ValueError("LINE_CHANNEL_SECRET is not set.")
#     if not settings.CHANNEL_ACCESS_TOKEN:
#         raise ValueError("LINE_CHANNEL_ACCESS_TOKEN is not set.")
        