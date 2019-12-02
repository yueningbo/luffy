from rest_framework import serializers
from .models import CourseCategory, Teacher, Course, CourseLesson, CourseChapter


class CourseCategoryModelSerializer(serializers.ModelSerializer):
    """课程分类的序列化器"""

    class Meta:
        model = CourseCategory
        fields = ["id", "name"]


class TeacherModelSerializer(serializers.ModelSerializer):
    """课程所属老师的序列化器"""

    class Meta:
        model = Teacher
        fields = ("name", "title", "signature")


class CourseModelSerializer(serializers.ModelSerializer):
    """课程信息的序列化器"""
    teacher = TeacherModelSerializer()  # 老师 1 : 多课程

    # teacher = CourseTeacherModelSerializer(many=True) # 多对1
    class Meta:
        model = Course
        fields = ("id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher")


class CourseLessonModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseLesson
        fields = ("id", "name", "free_tail")


class CourseChapterModelSerializer(serializers.ModelSerializer):
    course_sections = CourseLessonModelSerializer(many=True)  # 一个章节有多个课时, 所以many=True

    class Meta:
        model = CourseChapter
        fileds = ("id", "name", "course_sections")


class CourseModelSerializer(serializers.ModelSerializer):
    teacher = TeacherModelSerializer()
    course_chapters = CourseChapterModelSerializer(many=True)

    class Meta:
        model = Course
        fields = (
            "id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher", "course_chapters")
