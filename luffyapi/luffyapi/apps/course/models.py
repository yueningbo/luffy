from django.db import models
from luffyapi.utils.models import BaseModel
from ckeditor_uploader.fields import RichTextUploadingField


# Create your models here.
class CourseCategory(BaseModel):
    """课程分类"""
    name = models.CharField(max_length=64, unique=True, verbose_name='分类名称')

    class Meta:
        db_table = 'ly_course_category'
        verbose_name = '课程分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Course(BaseModel):
    """实战课程"""
    course_type_choices = (
        (0, "付费"),
        (1, "VIP专享"),
        (2, "学位课程")
    )
    level_choices = (
        (0, "初级"),
        (1, "中级"),
        (2, "高级")
    )
    status_choices = (
        (0, "上线"),
        (1, "下线"),
        (2, "预上线")
    )

    name = models.CharField(max_length=128, verbose_name="课程名称")
    course_img = models.ImageField(upload_to="course", max_length=255, verbose_name="封面图片", blank=True, null=True)
    course_type = models.SmallIntegerField(choices=course_type_choices, default=0, verbose_name="付费类型")
    # 使用这个字段的原因
    brief = RichTextUploadingField(verbose_name="详情介绍", null=True, blank=True)
    level = models.SmallIntegerField(choices=level_choices, default=1, verbose_name="难度等级")
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)
    period = models.IntegerField(verbose_name="建议学习周期(day)", default=7)
    attachment_path = models.FileField(upload_to="course_attachment", max_length=255, verbose_name="课件路径", blank=True,
                                       null=True)
    status = models.SmallIntegerField(choices=status_choices, default=0, verbose_name="课程状态")
    course_category = models.ForeignKey("CourseCategory", on_delete=models.DO_NOTHING, null=True, blank=True,
                                        verbose_name="课程分类")
    students = models.IntegerField(verbose_name="学习人数", default=0)
    lessons = models.IntegerField(verbose_name="总课时数量", default=0)
    pub_lessons = models.IntegerField(verbose_name="课时更新数量", default=0)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程原价", default=0)
    teacher = models.ForeignKey("Teacher", on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="授课老师")

    course_video = models.FileField(upload_to="course", max_length=255, verbose_name="封面视频", blank=True, null=True)

    class Meta:
        db_table = "ly_course"
        verbose_name = "专题课程"
        verbose_name_plural = "专题课程"

    def __str__(self):
        return "%s" % self.name

    @property
    def lesson_list(self):
        """课程列表的推荐课时"""
        data_list = self.course_lesson.filter(is_recommend=True)
        if len(data_list) < 1:
            return []

        data = []
        for item in data_list:
            data.append({
                "id": item.id,
                "name": item.name,
                "lesson": item.lesson,
                "section_type": item.section_type,
                "section_link": item.section_link,
                "free_trail": item.free_trail,
            })
        return data

    @property
    def get_expire_list(self):
        """当前课程所属的有效期选项"""
        data_list = []
        # 1. 再获取课程有效期选项的价格列表
        expire_list = self.course_expire.filter(is_show=True, is_deleted=False)
        for item in expire_list:
            data_list.append({
                "expire_time": item.expire_time,
                "expire_text": item.expire_text,
                "price": item.price,
            })

        # 2. 先获取当前课程的价格
        if self.price > 0:
            data_list.append({
                "expire_time": 0,
                "expire_text": "永久有效",
                "price": self.price,
            })

        return data_list

    @property
    def level_text(self):
        return self.level_choices[self.level][1]

    def real_price(self, expire_time):
        """根据有效期选项获取真实价格"""
        price = self.price
        # 如果购物车中的有效期选项非0,则表示有其他的有效期选项,则提取对应选项的价格
        if expire_time > 0:
            courseexpire = self.course_expire.get(expire_time=expire_time)
            price = courseexpire.price

        return price


class Teacher(BaseModel):
    """讲师、导师表"""
    role_choices = (
        (0, '讲师'),
        (1, '导师'),
        (2, '班主任'),
    )
    name = models.CharField(max_length=32, verbose_name="讲师title")
    role = models.SmallIntegerField(choices=role_choices, default=0, verbose_name="讲师身份")
    title = models.CharField(max_length=64, verbose_name="职位、职称")
    signature = models.CharField(max_length=255, verbose_name="导师签名", help_text="导师签名", blank=True, null=True)
    image = models.ImageField(upload_to="teacher", null=True, verbose_name="讲师封面")
    brief = models.TextField(max_length=1024, verbose_name="讲师描述")

    class Meta:
        db_table = "ly_teacher"
        verbose_name = "讲师导师"
        verbose_name_plural = "讲师导师"

    def __str__(self):
        return "%s" % self.name


class CourseChapter(BaseModel):
    """课程章节"""
    course = models.ForeignKey("Course", related_name='course_chapters', on_delete=models.CASCADE, verbose_name="课程名称")
    chapter = models.SmallIntegerField(verbose_name="第几章", default=1)
    name = models.CharField(max_length=128, verbose_name="章节标题")
    summary = models.TextField(verbose_name="章节介绍", blank=True, null=True)
    pub_date = models.DateField(verbose_name="发布日期", auto_now_add=True)

    class Meta:
        db_table = "ly_course_chapter"
        verbose_name = "课程章节"
        verbose_name_plural = "课程章节"

    def __str__(self):
        return "%s:(第%s章)%s" % (self.course, self.chapter, self.name)

    @property
    def lesson_list(self):
        """章节下的课时列表"""
        lessons = self.chaper_lesson.filter(is_show=True, is_deleted=False)
        data = []
        for lesson in lessons:
            data.append({
                "id": lesson.id,
                "name": lesson.name,
                "lesson": lesson.lesson,
                "section_type": lesson.section_type,
                "section_link": lesson.section_link,
                "duration": lesson.duration,
                "free_trail": lesson.free_trail,
            })

        return data


class CourseLesson(BaseModel):
    """
    课程课时
    """
    section_type_choices = (
        (0, '文档'),
        (1, '练习'),
        (2, '视频')
    )
    chapter = models.ForeignKey("CourseChapter", related_name='chaper_lesson', on_delete=models.CASCADE,
                                verbose_name="课程章节")
    course = models.ForeignKey("Course", related_name="course_lesson", on_delete=models.CASCADE, verbose_name="课程名称")
    name = models.CharField(max_length=128, verbose_name="课时标题")
    lesson = models.IntegerField(default=1, verbose_name="第几课时")
    section_type = models.SmallIntegerField(default=2, choices=section_type_choices, verbose_name="课时种类")
    section_link = models.CharField(max_length=255, blank=True, null=True, verbose_name="课时链接",
                                    help_text="若是video，填vid,若是文档，填link")
    duration = models.CharField(verbose_name="视频时长", blank=True, null=True, max_length=32)  # 仅在前端展示使用
    pub_date = models.DateTimeField(verbose_name="发布时间", auto_now_add=True)
    free_trail = models.BooleanField(verbose_name="是否可试看", default=False)
    is_recommend = models.BooleanField(verbose_name="是否推荐到课程列表", default=False)

    class Meta:
        db_table = "ly_course_lesson"
        verbose_name = "课程课时"
        verbose_name_plural = "课程课时"

    def __str__(self):
        return "%s-%s" % (self.chapter, self.name)


class CourseExpire(BaseModel):
    """课程有效期模型"""
    # 后面必须在数据库把course和expire_time字段设置为联合索引
    course = models.ForeignKey("Course", related_name='course_expire', on_delete=models.CASCADE,
                               verbose_name="课程名称")
    expire_time = models.IntegerField(verbose_name="有效期", null=True, blank=True, help_text="有效期按天数计算")
    expire_text = models.CharField(max_length=150, verbose_name="提示文本", null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="课程价格", default=0)

    class Meta:
        db_table = "ly_course_expire"
        verbose_name = "课程有效期"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "课程：%s，有效期：%s，价格：%s" % (self.course, self.expire_text, self.price)

    @classmethod
    def get_expire_text(cls, course_id, expire_time):
        """获取根据当前的有效期天数获取有效期显示文本"""
        if expire_time == 0:
            expire_text = "永久有效"
        else:
            course_expire = CourseExpire.objects.get(course_id=course_id, expire_time=expire_time)
            expire_text = course_expire.expire_text
        return expire_text
