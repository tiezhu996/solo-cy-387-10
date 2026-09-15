from django.conf import settings
from django.db import models

from app.constants.enums import USER_ROLES, ROLE_TENANT


class Profile(models.Model):
    """用户资料，记录平台角色（房东/租客/物业人员）。"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=[(r, r) for r in USER_ROLES], default=ROLE_TENANT)

    def __str__(self) -> str:
        return f'{self.user.username}({self.role})'
