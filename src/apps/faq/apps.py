from django.apps import AppConfig


class FaqConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "apps.faq"   # ← 重點：寫完整點號路徑
