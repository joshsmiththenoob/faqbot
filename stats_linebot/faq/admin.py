from django.contrib import admin
from .models import FAQ
from .utils import get_embedding

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "enabled")
    search_fields = ("question", "aliases")
    list_filter = ("enabled",)

    def save_model(self, request, obj, form, change):
        need_embed = False
        if not change:  # 新增
            need_embed = True
        elif "question" in getattr(form, "changed_data", []):  # 只有問題變更才重算
            need_embed = True

        if need_embed or obj.embedding is None:
            obj.embedding = get_embedding(obj.question)

        super().save_model(request, obj, form, change)
