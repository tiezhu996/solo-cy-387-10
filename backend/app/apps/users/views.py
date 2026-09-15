from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from app.utils.errors import auth_invalid
from app.utils.logger import get_logger
from .serializers import LoginSerializer, serialize_user

logger = get_logger('users')


class LoginView(APIView):
    """账号密码登录，返回 JWT 访问令牌与用户信息。"""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            request,
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )
        if user is None:
            logger.info('登录失败: %s', serializer.validated_data['username'])
            raise auth_invalid()
        token = RefreshToken.for_user(user)
        logger.info('登录成功: %s', user.username)
        return Response({'token': str(token.access_token), 'user': serialize_user(user)})


class MeView(APIView):
    """返回当前登录用户信息，用于刷新页面后恢复登录态。"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(serialize_user(request.user))
