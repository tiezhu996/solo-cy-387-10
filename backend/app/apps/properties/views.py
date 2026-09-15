from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from app.constants.enums import ROLE_LANDLORD, STATUS_OFFLINE
from app.utils.errors import not_found, permission_denied
from app.utils.logger import get_logger
from .models import Property
from .serializers import PropertySerializer

logger = get_logger('properties')


class PropertyListView(APIView):
    """房源列表：仅展示未下架房源，支持区域/价格/户型筛选。"""

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
        serializer = PropertySerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class PropertyDetailView(APIView):
    """房源详情：照片、描述、设施、房东联系方式，已下架也可查看但标记不可预约。"""

    permission_classes = [AllowAny]

    def get(self, request, property_id: int):
        try:
            prop = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            raise not_found()
        serializer = PropertySerializer(prop, context={'request': request})
        return Response(serializer.data)


class PropertyDelistView(APIView):
    """房东下架房源：状态置为已下架，收藏夹读取时立即标记失效。"""

    permission_classes = [IsAuthenticated]

    def post(self, request, property_id: int):
        profile = getattr(request.user, 'profile', None)
        if profile is None or profile.role != ROLE_LANDLORD:
            raise permission_denied('仅房东可以下架房源')
        try:
            prop = Property.objects.get(id=property_id)
        except Property.DoesNotExist:
            raise not_found()
        prop.status = STATUS_OFFLINE
        prop.save(update_fields=['status'])
        logger.info('房源下架: id=%s by=%s', prop.id, request.user.username)
        serializer = PropertySerializer(prop, context={'request': request})
        return Response(serializer.data)
