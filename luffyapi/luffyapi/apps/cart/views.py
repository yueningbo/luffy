from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated
from course.models import Course
from rest_framework.response import Response
import logging
from rest_framework import status
from django_redis import get_redis_connection
from luffyapi.settings import constants
from course.models import CourseExpire

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

        # 检测商品是否已存在
        if redis_conn.hget('cart_%s' % user_id, course_id):
            return Response({"message": "商品已存在, 不能重复添加!"}, status=status.HTTP_204_NO_CONTENT)

        # 保存数据到redis
        try:
            pipe = redis_conn.pipeline()
            pipe.multi()
            pipe.hset("cart_%s" % user_id, course_id, expire)
            pipe.sadd("selected_%s" % user_id, course_id)
            pipe.execute()

            # 查询购物车中商品总数
            cart_length = redis_conn.hlen("cart_%s" % user_id)
        except Exception as e:
            log.error("[Redis]购物车数据存储错误!\n错误:%s" % e)
            return Response({"message": "参数有误！购物车添加商品失败！"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        return Response({"message": "购物车商品添加成功！", "cart_length": cart_length})

    def get(self, request):
        """购物车列表"""
        user_id = request.user.id
        redis_conn = get_redis_connection('cart')

        cart_course_list = redis_conn.hgetall("cart_%s" % user_id)

        cart_selected_list = redis_conn.smembers("selected_%s" % user_id)

        if len(cart_course_list) < 1:
            return Response([])

        data = []

        for course_id_bytes, expire_time_bytes in cart_course_list.items():
            course_id = course_id_bytes.decode()
            expire_time = int(expire_time_bytes.decode())
            try:
                course = Course.objects.get(pk=course_id)
                data.append({
                    "course_id": course_id,
                    "name": course.name,
                    "course_img": constants.SERVER_IMAGE_URL + course.course_img.url,
                    "course_name": course.name,
                    "price": course.original_price(expire_time),
                    "real_price": course.real_price(expire_time),
                    "selected": True if course_id_bytes in cart_selected_list else False,
                    "expire_list": course.get_expire_list,  # 当前商品课程所有的有效期选项列表
                    "expire": expire_time,  # 购物车中当前商品的勾选有效期
                })
            except Course.DoesNotExist:
                pass
        return Response(data)

    def change_course_status(self, request):
        """更新修改状态"""
        # 获取前端传过来的信息
        user_id = request.user.id
        course_id = request.data.get("course_id")
        selected = request.data.get("selected")

        # 连接redis, 确认商品状态
        print(user_id, course_id, selected)
        redis_conn = get_redis_connection("cart")
        if selected:
            """添加勾选状态"""
            redis_conn.sadd("selected_%s" % user_id, course_id)
        else:
            """取消勾选状态"""
            redis_conn.srem("selected_%s" % user_id, course_id)
        return Response({"message": "切换商品勾选状态成功！"})

    def change_course_expire(self, request):
        """更新用户购物车的商品有效期选项"""
        # 获取客户端的信息[course_id, user_id ,expire_time]
        user_id = request.user.id
        course_id = request.data.get("course_id")
        expire_time = request.data.get("expire_time")

        # 连接redis，修改购物车中商品的有效期选项
        redis_conn = get_redis_connection("cart")
        redis_conn.hset("cart_%s" % user_id, course_id, expire_time)
        return Response({"message": "切换商品有效期选项成功！"})

    def get_selected_course(self, request):
        """获取购物车中勾选的商品信息"""
        user_id = request.user.id

        redis_conn = get_redis_connection("cart")

        cart_hash = redis_conn.hgetall("cart_%s" % user_id)
        selected_set = redis_conn.smembers("selected_%s" % user_id)

        data = []

        print("cart_hash==>", cart_hash)
        for course_id_bytes in selected_set:
            print("course_id_bytes==>", course_id_bytes)
            print("cart_hash.get(course_id_bytes)==>", cart_hash.get(course_id_bytes))
            course_id = course_id_bytes.decode()
            expire_time = int(cart_hash.get(course_id_bytes).decode())

            try:
                course = Course.objects.get(pk=course_id)
                data.append({
                    "course_id": course.id,
                    "course_img": constants.SERVER_IMAGE_URL + course.course_img.url,  # 返回图片的url地址
                    "course_name": course.name,
                    "price": course.original_price(expire_time),  # 商品原价
                    "real_price": course.real_price(expire_time),  # 折扣以后的价格
                    "selected": True if course_id_bytes in selected_set else False,
                    "expire_text": CourseExpire.get_expire_text(course_id, expire_time)
                })
            except CourseExpire.DoesNotExist:
                pass

        return Response(data)

    def delete(self, request):
        pass
