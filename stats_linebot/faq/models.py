from django.db import models
from pgvector.django import VectorField

class FAQ(models.Model):
    question = models.CharField(max_length=200, unique=True)
    answer   = models.TextField()
    aliases  = models.JSONField(default=list)
    enabled  = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 👇 新增語意向量（以 768 維為例；用哪個 embedding 模型就放幾維）
    # 向量可為空，建立時不用手動輸入
    embedding = VectorField(dimensions=768, null=True, blank=True)

    def __str__(self):
        return self.question

