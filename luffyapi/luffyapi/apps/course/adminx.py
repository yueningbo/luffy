import xadmin

from .models import CourseCategory
from .models import Course
from .models import Teacher
from .models import CourseChapter
from .models import CourseLesson


class CourseCategoryModelAdmin(object):
    """课程分类管理模型"""
    pass


xadmin.site.register(CourseCategory, CourseCategoryModelAdmin)


class CourseModelAdmin(object):
    list_display = ['name', 'course_img']
    list_editable = ['course_img']
    """课程模型管理类"""
    pass


xadmin.site.register(Course, CourseModelAdmin)


class TeacherModelAdmin(object):
    """老师模型管理类"""
    pass


xadmin.site.register(Teacher, TeacherModelAdmin)


class CourseChapterModelAdmin(object):
    """课程章节模型管理类"""
    pass


xadmin.site.register(CourseChapter, CourseChapterModelAdmin)


class CourseLessonModelAdmin(object):
    """课程课时模型管理类"""
    pass


xadmin.site.register(CourseLesson, CourseLessonModelAdmin)
