from django.db import models

from app.constants.enums import HOUSE_STATUS


class Property(models.Model):
    community = models.CharField(max_length=80)
    region = models.CharField(max_length=40)
    layout = models.CharField(max_length=20)
    area = models.IntegerField()
    rent = models.IntegerField()
    deposit = models.IntegerField()
    payment = models.CharField(max_length=20)
    facilities = models.JSONField(default=list)
    description = models.TextField(default='')
    photos = models.JSONField(default=list)
    status = models.CharField(max_length=20, choices=[(s, s) for s in HOUSE_STATUS], default='待出租')
    landlord_phone = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
