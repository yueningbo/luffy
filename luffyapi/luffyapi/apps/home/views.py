
# Create your views here.
from rest_framework.generics import ListAPIView
# 光标移动到要导报的类名或函数名或对象名或变量名，Alt+Enter 自动导包
from .models import Banner
from .serializers import BannerModelSerializer
from luffyapi.settings import constants

class BannerListAPIView(ListAPIView):
    queryset = Banner.objects.filter(is_show=True, is_deleted=False).order_by("orders","-id")[:constants.HOME_BANNER_LENGTH]
    serializer_class = BannerModelSerializer