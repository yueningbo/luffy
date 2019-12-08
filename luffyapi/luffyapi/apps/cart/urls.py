from django.urls import path, re_path
from . import views

urlpatterns = [
    path(r'', views.CartViewSet.as_view({"post": "post"})),
]
