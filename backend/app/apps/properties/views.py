from django.db.models import Count, Q
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.constants.enums import ROLE_LANDLORD, STATUS_OFFLINE
from app.utils.errors import not_found, permission_denied
from app.utils.logger import get_logger
from .models import Property
from .serializers import PropertyCreateSerializer, PropertySerializer

logger = get_logger('properties')


def _is_landlord(user) -> bool:
    profile = getattr(user, 'profile', None)
    return profile is not None and profile.role == ROLE_LANDLORD


def with_favorite_stats(queryset, user):
    """批量注解收藏总数与当前用户收藏状态，避免序列化时逐条查询（N+1）。

    无论列表多长，收藏统计都合并进主查询一次完成，查询次数与条数无关。
    """
    queryset = queryset.annotate(favorite_count=Count('favorited_by', distinct=True))
    if user.is_authenticated:
        queryset = queryset.annotate(
            viewer_favorite_count=Count('favorited_by', filter=Q(favorited_by__user=user), distinct=True),
        )
    return queryset


class PropertyListView(APIView):
    """房源列表：仅展示未下架房源，支持区域/价格/户型筛选。

    POST 为发布房源入口：仅房东可发布，归属强制设为当前登录房东。
    """

    permission_classes = [AllowAny]

    def get(self, request):
        queryset = Property.objects.exclude(status=STATUS_OFFLINE).order_by('id')
        region = request.query_params.get('region')
        layout = request.query_params.get('layout')
        max_rent = request.query_params.get('maxRent')
        if region:
            queryset = queryset.filter(region__contains=region)
        if layout and layout != '全部':
            queryset = queryset.filter(layout=layout)
        if max_rent and max_rent.isdigit():
            queryset = queryset.filter(rent__lte=int(max_rent))
        queryset = with_favorite_stats(queryset, request.user)
        serializer = PropertySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            raise permission_denied('请先登录')
        if not _is_landlord(request.user):
            raise permission_denied('仅房东可以发布房源')
        serializer = PropertyCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        prop = serializer.save(landlord=request.user)
        logger.info('房源发布: id=%s landlord=%s', prop.id, request.user.username)
        output = PropertySerializer(prop, context={'request': request})
        return Response(output.data, status=status.HTTP_201_CREATED)


class PropertyDetailView(APIView):
    """房源详情：照片、描述、设施、房东联系方式，已下架也可查看但标记不可预约。"""

    permission_classes = [AllowAny]

    def get(self, request, property_id: int):
        try:
            prop = with_favorite_stats(Property.objects.all(), request.user).get(id=property_id)
        except Property.DoesNotExist:
            raise not_found()
        serializer = PropertySerializer(prop, context={'request': request})
        return Response(serializer.data)


class PropertyDelistView(APIView):
    """房东下架房源：仅房源归属房东本人可操作。

    归属不符时直接拒绝，不修改房源状态，既有收藏关系保持不变。
    下架成功后状态置为已下架，收藏夹读取时立即标记失效。
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, property_id: int):
        if not _is_landlord(request.user):
            raise permission_denied('仅房东可以下架房源')
        try:
            prop = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            raise not_found()
        if prop.landlord_id != request.user.id:
            logger.info(
                '越权下架被拒绝: property=%s owner=%s operator=%s',
                prop.id, prop.landlord_id, request.user.id,
            )
            raise permission_denied('只能下架自己名下的房源')
        prop.status = STATUS_OFFLINE
        prop.save(update_fields=['status'])
        logger.info('房源下架: id=%s by=%s', prop.id, request.user.username)
        serializer = PropertySerializer(prop, context={'request': request})
        return Response(serializer.data)
