from rest_framework import serializers

from app.apps.properties.serializers import PropertySerializer
from app.constants.enums import STATUS_OFFLINE
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    """收藏夹条目：附带房源快照与有效标记，房源下架时 valid=False。"""

    propertyId = serializers.IntegerField(source='property_id')
    property = serializers.SerializerMethodField()
    valid = serializers.SerializerMethodField()
    createdAt = serializers.DateTimeField(source='created_at')

    class Meta:
        model = Favorite
        fields = ['id', 'propertyId', 'property', 'valid', 'createdAt']

    def get_property(self, obj) -> dict:
        return PropertySerializer(obj.property, context=self.context).data

    def get_valid(self, obj) -> bool:
        return obj.property.status != STATUS_OFFLINE
