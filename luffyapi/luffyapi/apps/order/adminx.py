import xadmin
from .models import Order
from .models import OrderDetail


class OrderModelAdmin(object):
    pass


xadmin.site.register(Order, OrderModelAdmin)


class OrderDetailModelAdmin(object):
    pass


xadmin.site.register(OrderDetail, OrderDetailModelAdmin)
