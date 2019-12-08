from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import OrderModelSerializer
from .models import Order


class OrderAPIView(CreateAPIView):
    """生成订单"""
    serializer_class = OrderModelSerializer
    queryset = Order.objects.filter(is_show=True, is_deleted=False)
