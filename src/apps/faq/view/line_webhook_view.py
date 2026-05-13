from django.views import View
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, HttpRequest
from apps.faq.dispatcher.line_webhook_dispatcher import LineWebhookDispatcher
from apps.faq.models import FAQ


class LineWebhookView(View):

    def post(self, request: HttpRequest, *args, **kwargs):
        # 獲取 X-Line-Signature 和 request body
        signature = request.headers.get("X-Line-Signature", "")
        body = request.body.decode("utf-8") if (request.body) else ""

        webhook_service = LineWebhookDispatcher()  

        # print("Signature:", signature, "\n", "Type:", type(signature), "\n", "Body:", body, "\n", "Type:", type(body))
        try:
            # the main service could be regarded as a dispatcher that dispatches event to different handlers
            # If event handler process susscessfully, it will send request to LINEBOT Messaging API to reply to user
            
            webhook_service.handle_webhook(body, signature)
            return HttpResponse(status=200)
        except Exception as e:
            # Otherwise it will raise exception and we can log the error for debugging
            print(f"Error handling request: {e}")
            return HttpResponse(status=500)
        
    