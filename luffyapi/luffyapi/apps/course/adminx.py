import xadmin

from .models import CourseCategory
from .models import Course
from .models import Teacher
from .models import CourseChapter
from .models import CourseLesson
from .models import CourseExpire


class CourseCategoryModelAdmin(object):
    """课程分类管理模型"""
    list_display = ["id", "name", "is_show"]
    list_editable = ["is_show"]


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


class CourseExpireModelAdmin(object):
    """商品有效期模型"""
    pass


xadmin.site.register(CourseExpire, CourseExpireModelAdmin)

"""价格优惠相关模型的注册"""

from .models import CourseDiscountType


class CourseDiscountTypeModelAdmin(object):
    """价格优惠类型"""
    pass


xadmin.site.register(CourseDiscountType, CourseDiscountTypeModelAdmin)

from .models import CourseDiscount


class CourseDiscountModelAdmin(object):
    """价格优惠公式"""
    pass


xadmin.site.register(CourseDiscount, CourseDiscountModelAdmin)

from .models import CoursePriceDiscount


class CoursePriceDiscountModelAdmin(object):
    """商品优惠和活动的关系"""
    pass


xadmin.site.register(CoursePriceDiscount, CoursePriceDiscountModelAdmin)

from .models import Activity


class ActivityModelAdmin(object):
    """商品活动模型"""
    pass


xadmin.site.register(Activity, ActivityModelAdmin)
