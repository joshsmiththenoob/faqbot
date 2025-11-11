from django.contrib import admin
from django.urls import path
from apps.faq.views import callback

urlpatterns = [
    path("admin/", admin.site.urls),
    path("callback", callback),  # LINE Webhook URL
]
