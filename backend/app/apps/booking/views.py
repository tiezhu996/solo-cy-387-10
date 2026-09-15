from rest_framework.response import Response
from rest_framework.views import APIView

from app.apps.properties.models import Property
from app.constants.enums import STATUS_OFFLINE
from app.utils.errors import not_found, property_offline
from app.utils.logger import get_logger

logger = get_logger('booking')


class BookingCreateView(APIView):
    """创建预约看房。已下架房源禁止预约；未传 propertyId 时保持原有演示行为。"""

    def post(self, request):
        property_id = request.data.get('propertyId')
        slot = request.data.get('slot', '周六 10:00')
        if property_id:
            try:
                prop = Property.objects.get(id=property_id)
            except Property.DoesNotExist:
                raise not_found()
            if prop.status == STATUS_OFFLINE:
                raise property_offline('房源已下架，无法预约看房')
            logger.info('预约创建: property=%s slot=%s', prop.id, slot)
            return Response({'id': 1001, 'propertyId': prop.id, 'status': '待房东确认', 'slot': slot})
        return Response({'id': 1001, 'status': '待房东确认', 'slot': slot})
