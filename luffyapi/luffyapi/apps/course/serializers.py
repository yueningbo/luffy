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
    """
    课程信息的序列化器
    默认情况,序列化器转换模型数据时,默认会把外键直接转成主键ID值
    所以我们需要重新设置在序列化器中针对外键的序列化
    这种操作就是一个序列器里面调用另一个序列化器了.叫'序列化器嵌套'
    """
    teacher = TeacherModelSerializer()

    # course_chapters = CourseChapterModelSerializer(many=True)

    class Meta:
        model = Course
        fields = (
            "id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher", "course_chapters")
