from django.conf import settings
from django.http import (
    JsonResponse,
    HttpResponse,
    HttpResponseForbidden,
    HttpRequest
)
from django.views.decorators.csrf import csrf_exempt
from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.messaging import(
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    QuickReply,
    QuickReplyItem
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
from .utils import check_channel_config
from .models import FAQ
from rapidfuzz import (
    fuzz, 
    process
)
        

check_channel_config()
configuration = Configuration(access_token=settings.CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.CHANNEL_SECRET)


@csrf_exempt
def callback(request: HttpRequest) -> HttpResponse:
    if (request.method != "POST"):
        return HttpResponseForbidden("Only POST requests are allowed.")
    
    print("Received request:", request)

    print("Headers: ", request.headers)
    # Get X-Line-Signature header value
    signature = request.headers.get("X-Line-Signature", "")

    # Get request body as text
    body = request.body.decode("utf-8") if request.body else ""
    print("type of signature:", type(signature))
    print("type of body:", type(body))
    
    print("Signature:", signature, "\n", "Type:", type(signature), "\n", "Body:", body, "\n", "Type:", type(body))
    if not signature:
        print("Missing X-Line-Signature header.")
        return HttpResponseForbidden("Missing X-Line-Signature header.")
    
    try:
        handler.handle(body, signature)
        return HttpResponse(status=200)
    except Exception as e:
        print(f"Error handling request: {e}")
        return HttpResponse(status=500)