from django.views.generic import ListView
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden, HttpRequest
from faq.service.faq_service import FAQService
from faq.models import FAQ


class FAQListView(ListView):
    model = FAQ

    # def get(self, request, *args, **kwargs):
    #     # 在這裡處理 LINE Webhook 的回調邏輯
    #     pass

    def post(self, request: HttpRequest, *args, **kwargs):
        # 在這裡處理 LINE Webhook 的回調邏輯
        # signature = request.headers.get("X-Line-Signature", "")
        # body = request.body.decode("utf-8") if (request.body) else ""

        # print("Signature:", signature, "\n", "Type:", type(signature), "\n", "Body:", body, "\n", "Type:", type(body))
        try:
            faq_service = FAQService()  # 這裡的 parser 需要根據實際情況傳入
            # faq_service.handle_webhook(request)
            return HttpResponse(status=200)

    