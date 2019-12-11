from django.db import models
from luffyapi.utils.models import BaseModel
from ckeditor_uploader.fields import RichTextUploadingField
from luffyapi.settings import constants
from datetime import datetime


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
                "real_price": float(self.discount_price(item.price)),
                "price": float(item.price),
            })

        # 2. 先获取当前课程的价格
        if self.price > 0:
            data_list.append({
                "expire_time": 0,
                "expire_text": "永久有效",
                "real_price": float(self.discount_price(self.price)),
                "price": float(self.price),
            })

        return data_list

    @property
    def level_text(self):
        return self.level_choices[self.level][1]

    def original_price(self, expire_time):
        """根据有效期选项获取真实价格"""
        price = self.price
        # 如果购物车中的有效期选项非0,则表示有其他的有效期选项,则提取对应选项的价格
        if expire_time > 0:
            course_expire = self.course_expire.get(expire_time=expire_time)
            price = course_expire.price

        return price

    def real_price(self, expire_time):
        """根据有效期选项获取真实价格"""
        price = self.price
        # 如果购物车中的有效期选项非0,则表示有其他的有效期选项,则提取对应选项的价格
        if expire_time > 0:
            courseexpire = self.course_expire.get(expire_time=expire_time)
            price = courseexpire.price

        result = self.get_activity
        if result != "":
            price = float(self.discount_price(price))

        return price

    @property
    def discount_name(self):
        """当前课程参与的优惠类型"""
        # 判断当前课程是否参与了活动，如果有参与了活动，是否处于活动时间范围内
        result = self.get_activity
        if result == "":
            return result
        # 返回活动中商品的优惠类型
        return result.discount.discount_type.name

    @property
    def get_activity(self):
        try:
            result = self.activePrices.get(is_show=True, is_deleted=False, active__start_time__lte=datetime.now(),
                                           active__end_time__gt=datetime.now())
            return result
        except CoursePriceDiscount.DoesNotExist:
            # 查询当前课程如果没有参与到活动中，则直接返回空字符串
            return ""

    def discount_price(self, price=None):
        """当前课程参与活动以后的优惠实价"""
        # 判断当前课程是否参与了活动，如果有参与了活动，是否处于活动时间范围内
        result = self.get_activity
        if result == "":
            return 0

        # 根据优惠公式，计算新的价格
        if price is None:
            price = self.price  # 原价

        price = float(price)
        sale = result.discount.sale  # 价格优惠公式
        if sale == "":
            """限时免费"""
            price = 0

        elif sale[0] == "*":
            """限时折扣"""
            price = price * float(sale[1:])

        elif sale[0] == "-":
            """限时减免"""
            price = price - float(sale[1:])

        elif sale[0] == "满":
            sale_list = sale.split("\r\n")
            discount_list = []
            for sale_item in sale_list:
                item_price, discount = sale_item.split("-")
                if float(item_price[1:]) < price:
                    discount_list.append(float(discount))

            price = price - max(discount_list)

        return "%.2f" % price

    @property
    def activity_time(self):
        """当前课程参与活动的剩余时间"""
        # 判断当前课程是否参与了活动，如果有参与了活动，是否处于活动时间范围内
        result = self.get_activity
        has_time = -1
        if result != "":
            # 活动结束时间
            end_time = result.active.end_time.timestamp()
            # 当前服务器时间
            now_time = datetime.now().timestamp()
            # 剩余时间= 活动结束 - 当前时间
            has_time = end_time - now_time

        return int(has_time)


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


"""价格相关模型"""


class CourseDiscountType(BaseModel):
    """课程优惠类型"""
    name = models.CharField(max_length=32, verbose_name="优惠类型名称")
    remake = models.CharField(max_length=250, blank=True, null=True, verbose_name="备注信息")

    class Meta:
        db_table = "ly_course_discount_type"
        verbose_name = "课程优惠类型"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "%s" % (self.name)


class CourseDiscount(BaseModel):
    discount_type = models.ForeignKey("CourseDiscountType", on_delete=models.CASCADE, related_name='courseDiscounts',
                                      verbose_name="优惠类型")
    condition = models.IntegerField(blank=True, default=0, verbose_name="满足优惠的价格条件",
                                    help_text="设置参与优惠的价格门槛, 表示商品必须在xx价格以上的时候才参与优惠活动,<br>如果不填,则不设置门槛")
    sale = models.TextField(verbose_name="优惠公式", blank=True, null=True, help_text="""
    不填表示免费；<br>
    *号开头表示折扣价，例如*0.82表示八二折；<br>
    -号开头则表示减免，例如-20表示原价-20；<br>
    如果需要表示满减,则需要使用 原价-优惠价格,例如表示课程价格大于100,优惠10;大于200,优惠20,格式如下:<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满100-10<br>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;满200-25<br>""")

    class Meta:
        db_table = 'ly_course_discount'
        verbose_name = "价格优惠策略"
        verbose_name_plural = "价格优惠策略"

    def __str__(self):
        return "价格优惠:%s, 优惠条件:%s, 优惠值:%s" % (self.discount_type.name, self.condition, self.sale)


class Activity(BaseModel):
    """优惠活动"""
    name = models.CharField(max_length=150, verbose_name="活动名称")
    start_time = models.DateTimeField(verbose_name="优惠策略开始时间")
    end_time = models.DateTimeField(verbose_name="优惠策略结束时间")
    remark = models.CharField(max_length=250, blank=True, null=True, verbose_name="备注信息")

    class Meta:
        db_table = "ly_activity"
        verbose_name = "商品活动"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CoursePriceDiscount(BaseModel):
    """课程与优惠策略的关系表"""
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="activePrices", verbose_name="课程")
    active = models.ForeignKey("Activity", on_delete=models.DO_NOTHING, related_name="activeCourses", verbose_name="活动")
    discount = models.ForeignKey("CourseDiscount", on_delete=models.CASCADE, related_name="discountCourse",
                                 verbose_name="优惠折扣")

    class Meta:
        db_table = 'ly_course_price_discount'
        verbose_name = "课程与优惠策略关系"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "课程:%s, 优惠活动: %s, 开始时间:%s, 结束时间:%s" % (
            self.course.name, self.active.name, self.active.start_time, self.active.end_time)
