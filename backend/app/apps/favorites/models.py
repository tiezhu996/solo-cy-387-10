from django.conf import settings
from django.db import models

from app.apps.properties.models import Property


class Favorite(models.Model):
    """收藏关系。(user, property) 唯一约束保证同一租客重复收藏只产生一条记录，
    收藏数始终通过 count 实时统计，不维护冗余计数，避免并发下计数错乱。"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'property'], name='uniq_favorite_user_property'),
        ]
