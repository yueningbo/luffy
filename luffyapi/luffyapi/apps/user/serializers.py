from rest_framework import serializers
from .models import User
import re
from .utils import get_user_by_account
from django.contrib.auth.hashers import make_password
from rest_framework_jwt.settings import api_settings
from django_redis import get_redis_connection


class UserModelSerializer(serializers.ModelSerializer):
    sms_code = serializers.CharField(min_length=4, max_length=6, required=True, write_only=True, help_text="短信验证码")
    token = serializers.CharField(max_length=1024, read_only=True, help_text="token认证字符串")

    class Meta:
        model = User
        fields = ["id", "username", "mobile", "password", "sms_code", "token"]
        extra_kwargs = {
            "id": {"read_only": True, },
            "username": {"read_only": True, },
            "password": {"write_only": True, "min_length": 6},
            "mobile": {"write_only": True, "min_length": 11},
        }

    def validate(self, attrs):
        mobile = attrs.get("mobile")
        # 验证手机号码格式
        if not re.match(r"1[3-9]\d{9}$", mobile):
            raise serializers.ValidationError("对不起,手机号格式有误!")

        # 验证码手机号是否已经注册过了
        try:
            User.objects.get(mobile=mobile)
            raise serializers.ValidationError("对不起，当前手机号已经被注册！")
        except User.DoesNotExist:
            pass

        # 验证短信是否正确
        user_sms = attrs.get("sms_code")
        redis_conn = get_redis_connection("sms_code")
        redis_sms = redis_conn.get("sms_%s" % mobile)
        if redis_sms is None:
            raise serializers.ValidationError("对不起，当前验证码已过期！")

        if redis_sms.decode() != user_sms:
            raise serializers.ValidationError("对不起，短信验证码错误！")

        return attrs

    def create(self, validated_date):
        validated_date.pop("sms_code")
        # 加密密码
        raw_password = validated_date.get("password")
        hash_password = make_password(raw_password)
        # 用户名设为默认值
        username = validated_date.get("mobile")
        mobile = validated_date.get("mobile")
        user = User.objects.create_user(mobile=mobile, username=username, password=hash_password)

        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)

        return user
