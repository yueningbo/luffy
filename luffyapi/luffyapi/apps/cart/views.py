from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from course.models import Course
from rest_framework.response import Response
import logging
from rest_framework import status
from django_redis import get_redis_connection

log = logging.getLogger("django")


class CartViewSet(ViewSet):
    """购物车"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """添加商品到购物车"""
        # 接受客户端提交参数[用户ID，课程ID，勾选状态，有效期选项]
        course_id = request.data.get("course_id")
        user_id = request.user.id
        # 设置默认值
        selected = True
        expire = 0  # 0 为永久有效

        # 验证提交的值
        try:
            course = Course.objects.get(is_show=True, is_deleted=False, id=course_id)
        except Course.DoesNotExist:
            return Response({"message": "参数有误,课程不存在!"}, status=status.HTTP_400_BAD_REQUEST)

        # 获取redis对象
        redis_conn = get_redis_connection("cart")

        # 保存数据到redis
        try:
            pipe = redis_conn.pipeline()
            pipe.multi()
            pipe.hset("cart_%s" % user_id, course_id, expire)
            pipe.sadd("selected_%s" % user_id, course_id)
            pipe.execute()

            # 查询购物车中商品总数
            course_len = redis_conn.hlen("cart_%s" % user_id)
        except Exception as e:
            log.error("[Redis]购物车数据存储错误!\n错误:%s" % e)
            return Response({"message": "参数有误！购物车添加商品失败！"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        return Response({"message": "购物车商品添加成功！", "length": course_len})
