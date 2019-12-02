from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import CourseCategory, Course
from .serializers import CourseCategoryModelSerializer
from .serializers import CourseModelSerializer


class CourseCategoryListAPIView(ListAPIView):
    queryset = CourseCategory.objects.filter(is_show=True, is_deleted=False).order_by("orders", "-id")
    serializer_class = CourseCategoryModelSerializer


class CourseListAPIView(ListAPIView):
    queryset = Course.objects.filter(is_deleted=False, is_show=True).order_by("orders", "id")
    serializer_class = CourseModelSerializer
