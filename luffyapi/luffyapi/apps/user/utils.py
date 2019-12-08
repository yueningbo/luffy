import re
from .models import User
from django.contrib.auth.backends import ModelBackend
from django_redis import get_redis_connection


def jwt_response_payload_handler(token, user=None, request=None):
    """自定义jwt认证成功返回数据"""
    redis_conn = get_redis_connection("cart")
    cart_length = redis_conn.hlen("cart_%s" % user.id)
    return {
        'token': token,
        'id': user.id,
        'username': user.username,
        'cart_length': cart_length,
    }


def get_user_by_account(account):
    """
    根据账号获取user对象
    :param account:账号, 可以是用户名或者手机号
    :return: User对象 或者 None
    """
    try:
        if re.match('^1[3-9]\d{9}', account):
            # 账号为手机号
            user = User.objects.get(mobile=account)
        else:
            # 账号为用户名
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户名或手机认证
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        if user is not None and user.check_password(password):
            return user
