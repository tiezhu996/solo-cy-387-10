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
        prop = obj.property
        # 把视图层批量注解的收藏统计挂到房源实例上，
        # PropertySerializer 会优先读取，避免逐条再查。
        favorite_count = getattr(obj, 'property_favorite_count', None)
        if favorite_count is not None:
            prop.favorite_count = favorite_count
        viewer_count = getattr(obj, 'property_viewer_favorite_count', None)
        if viewer_count is not None:
            prop.viewer_favorite_count = viewer_count
        return PropertySerializer(prop, context=self.context).data

    def get_valid(self, obj) -> bool:
        return obj.property.status != STATUS_OFFLINE
