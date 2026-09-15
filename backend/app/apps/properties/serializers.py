from rest_framework import serializers

from app.constants.enums import STATUS_OFFLINE
from .models import Property


class PropertySerializer(serializers.ModelSerializer):
    """列表/详情通用序列化，附带当前用户的收藏状态与收藏总数。"""

    landlordPhone = serializers.CharField(source='landlord_phone')
    favoriteCount = serializers.SerializerMethodField()
    favorited = serializers.SerializerMethodField()
    bookable = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'id', 'community', 'region', 'layout', 'area', 'rent', 'deposit', 'payment',
            'facilities', 'description', 'photos', 'status', 'landlordPhone',
            'favoriteCount', 'favorited', 'bookable',
        ]

    def get_favoriteCount(self, obj) -> int:
        return obj.favorited_by.count()

    def get_favorited(self, obj) -> bool:
        user = self.context.get('request').user if self.context.get('request') else None
        if not user or not user.is_authenticated:
            return False
        return obj.favorited_by.filter(user=user).exists()

    def get_bookable(self, obj) -> bool:
        return obj.status != STATUS_OFFLINE
