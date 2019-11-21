from django.urls import path
from . import views
urlpatterns = [
    path("banner/", views.BannerListAPIView.as_view() ),
]