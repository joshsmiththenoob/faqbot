from django.urls import path, include
from apps.faq.views import callback



urlpatterns = [
    path("callback/", callback),  # LINE Webhook URL
]
