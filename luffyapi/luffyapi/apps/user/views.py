from django.shortcuts import render

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
