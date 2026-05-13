"""
Duty of handle FollowEvent from event handler,
FollowEvent: When LINEBOT get a new friend(client), it build welcome message for User throught Message API from this service!!
"""



from linebot.v3.messaging import TextMessage


class FollowEventService:
    def __init__(self):
        pass

    def build_welcome_message(self) -> TextMessage:
        welcome_text = (
            "您好，歡迎使用主力農家問題 LINE Bot。\n\n"
            "您可以直接輸入想了解的問題，越具體越好。\n"
            "例如：農業保險、給付標準、調查資料填寫方式。\n\n"
            "我會協助您從常見問答中找出最接近的問題。"
        )

        return TextMessage(text=welcome_text)