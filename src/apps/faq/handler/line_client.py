from django.conf import settings
from linebot.v3 import WebhookParser
from linebot.v3.messaging import(
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
)
class LineClient():
    def __init__(self):
        self.__check_channel_config()
        
        configuration = Configuration(
            access_token= settings.CHANNEL_ACCESS_TOKEN
            )
        self._api_client = ApiClient(configuration)
        self._messaging_api = MessagingApi(self._api_client)


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
    def webhook_parser(self):
        return WebhookParser(settings.CHANNEL_SECRET)
    

    def reply_message(self, reply_token: str, messages: list) -> None:
        request = ReplyMessageRequest(
            reply_token=reply_token,
            messages=messages
        )
        self._messaging_api.reply_message(request)
    


            


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
        