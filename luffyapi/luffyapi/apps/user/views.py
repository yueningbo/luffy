from django.shortcuts import render
from django.http import response

# Create your views here.
pc_geetest_id = "5e876edb2bda195c265416b70e7389a7"
pc_geetest_key = "c1f0f6f5958507924d187db31cd136e5"

from luffyapi.libs.geetest import GeetestLib
from rest_framework.response import Response
from .utils import get_user_by_account
from rest_framework import status as http_status
from rest_framework.views import APIView


class CaptchaAPIView(APIView):
    """验证码视图类"""
    status = False
    user_id = 0

    def get(self, request):
        """获取验证码"""
        username = request.query_params.get("username")
        user = get_user_by_account(username)
        if user is None:
            return Response({"message": "对不起, 用户不存在!"}, status=http_status.HTTP_400_BAD_REQUEST)

        self.user_id = user.id
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        # todo 后面增加status和user_id保存到redis数据库
        response_str = gt.get_response_str()
        return Response(response_str)

    def post(self, request):
        """验证码的验证方法"""
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        if self.status:
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        result = {"status": "success"} if result else {"status": "fail"}
        return Response(result)


from luffyapi.libs.yuntongxun.sms import CCP
import random
from django_redis import get_redis_connection
from luffyapi.settings import constants


class SMSAPIView(APIView):
    def get(self, request, mobile):
        # 保存短信验证码与发送记录
        redis_conn = get_redis_connection('sms_code')
        ret = redis_conn.get("send_%s" % mobile)
        # 1. 判断是否冷却
        if ret is not None:
            return Response({})
        # 2. 生成短信验证码
        sms_code = "%06d" % random.randint(0, 999999)
        sms_time = constants.SMS_EXPIRE_TIME

        # 3. 发送短信
        ccp = CCP()
        ret = ccp.send_template_sms(mobile, [sms_code, sms_time // 60], 1)
        if ret == -1:
            return Response({"message": "短信发送失败![CCP]"})

        # 3.1 使用管道多次加载, 一次执行多个指令
        pl = redis_conn.pipeline()
        pl.multi()
        pl.setex("sms_%s" % mobile, sms_time, sms_code)  # 设置短信有效期
        pl.setex("sms_time_%s" % mobile, constants.SMS_INTERVAL_TIME, 1)  # 设置发送间隔时间
        pl.execute()

        return Response({"message": "短信发送成功!"})


from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import UserModelSerializer


class UserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


from rest_framework import status


class MobileAPIView(APIView):
    def get(self, request, mobile):
        # 验证手机号唯一性
        try:
            User.objects.get(mobile=mobile)
            return Response({"message": "当前手机号已被注册", "status": False}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"status": True}, status=status.HTTP_200_OK)
