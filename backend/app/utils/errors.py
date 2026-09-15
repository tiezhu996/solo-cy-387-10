from rest_framework import status
from rest_framework.exceptions import APIException

from app.constants.errors import ERROR_CODES


def make_error(code_key: str, message: str, http_status: int) -> APIException:
    """构造带业务错误码的 DRF 异常，由统一异常处理器包装输出。"""
    exc = APIException(detail={'code': ERROR_CODES[code_key], 'message': message})
    exc.status_code = http_status
    return exc


def not_found(message: str = '房源不存在') -> APIException:
    return make_error('PROPERTY_NOT_FOUND', message, status.HTTP_404_NOT_FOUND)


def property_offline(message: str = '房源已下架，无法继续操作') -> APIException:
    return make_error('PROPERTY_OFFLINE', message, status.HTTP_400_BAD_REQUEST)


def auth_invalid(message: str = '用户名或密码错误') -> APIException:
    return make_error('AUTH_INVALID', message, status.HTTP_401_UNAUTHORIZED)


def permission_denied(message: str = '没有权限执行该操作') -> APIException:
    return make_error('PERMISSION_DENIED', message, status.HTTP_403_FORBIDDEN)
