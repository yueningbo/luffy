from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.views.static import serve

import xadmin

xadmin.autodiscover()

# version模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion

xversion.register_models()

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),
    path('', include("home.urls")),
    path('xadmin/', xadmin.site.urls),
    path('user/', include("user.urls")),
    path('course/', include("course.urls"))
]
