from django.contrib import admin
from django.urls import path,  include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("line-bots/", include("apps.faq.urls")),  # LINE Webhook URL in faq app
]
