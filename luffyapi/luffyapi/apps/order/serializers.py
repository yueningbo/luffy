from rest_framework import serializers
from .models import Order,OrderDetail
from course.models import Course
from django_redis import get_redis_connection
from django.db import transaction

class OrderModelSerializer(serializers.ModelSerializer):
    """订单序列化器"""
    # 模型
    class Meta:
        model = Order
        fields = ["order_number","total_price","real_price","pay_type","credit","coupon"]
        read_only_fields = ["order_number", "total_price","real_price"]
        extra_kwargs = {
            "pay_type": {"write_only": True, "default": 1},
            "credit": {"write_only": True,"min_value": 0 },
            "coupon": {"write_only": True},
        }


    # 数据验证方法
    def validate(self, attrs):
        # todo credit

        # todo coupon

        return attrs

    # 模型的保存或者更新方法
    def create(self, validated_data):
        """保存订单"""
        pay_type = validated_data.get("pay_type")
        credit = validated_data.get("credit")
        coupon = validated_data.get("coupon")

        order_title = "路飞学城课程购买"
        total_price = 0
        real_price = 0
        # 时间+用户ID+随机数
        from datetime import datetime
        import random
        user_id = self.context["request"].user.id

        order_number = datetime.now().strftime("%Y%m%d%H%M%S") + ("%06d" % user_id) + ("%05d" % random.randint(0,99999))
        with transaction.atomic():
            save_id = transaction.savepoint() # 设置回滚点
            try:
                order = Order.objects.create(
                    order_title=order_title,
                    total_price=total_price,
                    real_price=real_price,
                    order_number=order_number,
                    order_status = 0,
                    pay_type=pay_type,
                    credit=credit,
                    coupon=coupon,
                    user_id=user_id
                )

                # 记录当前订单定义的课程信息到订单详情
                redis_conn = get_redis_connection("cart")
                cart_hash = redis_conn.hgetall("cart_%s" % user_id)
                selected_set = redis_conn.smembers("selected_%s" % user_id)

                # 开启redis事务
                pipe = redis_conn.pipeline()
                pipe.multi()

                for course_id_bytes in selected_set:
                    course_id = course_id_bytes.decode()
                    expire_time = int( cart_hash.get(course_id_bytes).decode() )

                    # 根据当前课程ID来获取课程信息
                    course = Course.objects.get(pk=course_id)

                    # 把课程信息添加到订单详情里面
                    order_detail = OrderDetail.objects.create(
                        order=order,
                        course=course,
                        expire=expire_time,
                        price=course.real_price(expire_time),
                        real_price=course.real_price(expire_time), # todo 将来完成优惠券或者积分的时候计算真实的价格
                        discount_name="原价购买", # todo 将来完成了优惠以后，这里进行调整
                    )

                    # 从购物车中删除对应的商品课程
                    pipe.hdel("cart_%s" % user_id, course_id)
                    pipe.srem("selected_%s" % user_id, course_id)
                    # todo 计算订单的总价格

                # 提交redis事务操作
                pipe.execute()

            except:
                transaction.savepoint_rollback(save_id)
                return serializers.ValidationError("订单生成失败！")

        return order