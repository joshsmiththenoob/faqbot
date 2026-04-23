from django.views import View
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, HttpRequest
from apps.faq.service.line_webhook_service import LineWebhookService
from faq.models import FAQ


class LineWebhookView(View):

    def post(self, request: HttpRequest, *args, **kwargs):
        # 獲取 X-Line-Signature 和 request body
        signature = request.headers.get("X-Line-Signature", "")
        body = request.body.decode("utf-8") if (request.body) else ""

        # print("Signature:", signature, "\n", "Type:", type(signature), "\n", "Body:", body, "\n", "Type:", type(body))
        try:
            webhook_service = LineWebhookService()  # 這裡的 parser 需要根據實際情況傳入
            # webhook_service.handle_webhook(body, signature)
            return HttpResponse(status=200)
        except Exception as e:
            print(f"Error handling request: {e}")
            return HttpResponse(status=500)
        
    