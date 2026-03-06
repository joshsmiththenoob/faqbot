from django.urls import path, include
from apps.faq.view_test import callback



urlpatterns = [
    path("callback/", callback),  # LINE Webhook URL
]
