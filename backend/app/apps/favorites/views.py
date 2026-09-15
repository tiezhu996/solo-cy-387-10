from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.apps.properties.models import Property
from app.constants.enums import STATUS_OFFLINE
from app.utils.errors import not_found, property_offline
from app.utils.logger import get_logger
from .models import Favorite
from .serializers import FavoriteSerializer

logger = get_logger('favorites')


class FavoriteListView(APIView):
    """当前登录用户的收藏夹，只返回本人的收藏，按收藏时间倒序。"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        favorites = (
            Favorite.objects.filter(user=request.user)
            .select_related('property')
            .order_by('-created_at', '-id')
        )
        serializer = FavoriteSerializer(favorites, many=True, context={'request': request})
        return Response(serializer.data)


class FavoriteStateView(APIView):
    """幂等设置收藏状态：PUT {favorite: true|false}。

    同一租客快速重复点击时，每次请求都收敛到请求指定的目标状态：
    - 收藏：唯一约束 + get_or_create，重复写不会产生重复记录；
    - 取消：filter().delete() 幂等，删多次与删一次结果一致。
    响应返回数据库中的最终状态与实时收藏数，前端以此为准。
    """

    permission_classes = [IsAuthenticated]

    def put(self, request, property_id: int):
        try:
            prop = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            raise not_found()

        favorite = bool(request.data.get('favorite'))
        if favorite and prop.status == STATUS_OFFLINE:
            raise property_offline('房源已下架，无法收藏')

        with transaction.atomic():
            if favorite:
                Favorite.objects.get_or_create(user=request.user, property=prop)
            else:
                Favorite.objects.filter(user=request.user, property=prop).delete()

        favorited = Favorite.objects.filter(user=request.user, property=prop).exists()
        favorite_count = Favorite.objects.filter(property=prop).count()
        logger.info('收藏状态: user=%s property=%s favorite=%s', request.user.username, prop.id, favorited)
        return Response({'propertyId': prop.id, 'favorited': favorited, 'favoriteCount': favorite_count})
