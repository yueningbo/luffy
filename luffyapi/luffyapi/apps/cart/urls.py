from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'', views.CartViewSet.as_view({"post": "post",
                                         "get": "get",
                                         "put": "change_course_status",
                                         "patch": "change_course_expire",
                                         "delete": "delete",
                                         })),
    path("order/", views.CartViewSet.as_view({"get": "get_selected_course"})),
]
