from django.shortcuts import render
from rest_framework.generics import ListAPIView
from .models import CourseCategory, Course, CourseChapter
from .serializers import CourseCategoryModelSerializer
from .serializers import CourseModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .paginations import CourseListPageNumberPagination
from rest_framework.generics import RetrieveAPIView
from .serializers import CourseRetrieveModelSerializer
from .serializers import CourseChapterModelSerializer


class CourseCategoryListAPIView(ListAPIView):
    queryset = CourseCategory.objects.filter(is_show=True, is_deleted=False).order_by("orders", "-id")
    serializer_class = CourseCategoryModelSerializer


class CourseListAPIView(ListAPIView):
    """课程列表API接口"""
    queryset = Course.objects.filter(is_show=True, is_deleted=False).order_by("orders", "-id")
    serializer_class = CourseModelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ('course_category',)
    ordering_fields = ['id', 'students', 'price']
    # 指定分页器
    pagination_class = CourseListPageNumberPagination


class CourseRetrieveAPIView(RetrieveAPIView):
    queryset = Course.objects.filter(is_show=True, is_deleted=False)
    serializer_class = CourseRetrieveModelSerializer


class CourseChapterListAPIView(ListAPIView):
    queryset = CourseChapter.objects.filter(is_deleted=False, is_show=True).order_by("chapter")
    serializer_class = CourseChapterModelSerializer
    filter_backends = [DjangoFilterBackend, ]
    filter_fields = ['course', ]
