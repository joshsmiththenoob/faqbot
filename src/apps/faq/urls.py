from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from apps.faq.view.line_webhook_view import LineWebhookView



urlpatterns = [
    # LINE Webhook URL -> Line Platform is authenticated by X-Line-Signature header,not CSRF token.
    # Just exempt CSRF check for this URL(endpoint).
    path("callback/", csrf_exempt(
                        LineWebhookView.as_view()
                        )),  
]
