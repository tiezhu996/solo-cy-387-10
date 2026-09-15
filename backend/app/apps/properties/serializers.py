from rest_framework import serializers

from app.constants.enums import STATUS_OFFLINE
from .models import Property


class PropertySerializer(serializers.ModelSerializer):
    """列表/详情通用序列化，附带归属、当前用户收藏状态与收藏总数。

    收藏统计优先读取视图层批量注解（favorite_count / viewer_favorite_count），
    未注解的单对象场景（详情、下架响应）回退到逐对象查询，两种路径结果一致。
    """

    landlordId = serializers.IntegerField(source='landlord_id', read_only=True)
    landlordPhone = serializers.CharField(source='landlord_phone')
    favoriteCount = serializers.SerializerMethodField()
    favorited = serializers.SerializerMethodField()
    bookable = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = [
            'id', 'landlordId', 'community', 'region', 'layout', 'area', 'rent', 'deposit', 'payment',
            'facilities', 'description', 'photos', 'status', 'landlordPhone',
            'favoriteCount', 'favorited', 'bookable',
        ]

    def get_favoriteCount(self, obj) -> int:
        annotated = getattr(obj, 'favorite_count', None)
        if annotated is not None:
            return annotated
        return obj.favorited_by.count()

    def get_favorited(self, obj) -> bool:
        user = self.context.get('request').user if self.context.get('request') else None
        if not user or not user.is_authenticated:
            return False
        annotated = getattr(obj, 'viewer_favorite_count', None)
        if annotated is not None:
            return annotated > 0
        return obj.favorited_by.filter(user=user).exists()

    def get_bookable(self, obj) -> bool:
        return obj.status != STATUS_OFFLINE


class PropertyCreateSerializer(serializers.ModelSerializer):
    """发布房源：归属由视图强制设为当前登录房东，不接受客户端传入。"""

    landlordPhone = serializers.CharField(source='landlord_phone')

    class Meta:
        model = Property
        fields = [
            'community', 'region', 'layout', 'area', 'rent', 'deposit', 'payment',
            'facilities', 'description', 'photos', 'landlordPhone',
        ]
