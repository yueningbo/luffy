from django.db import models

# Create your models here.
class Banner(models.Model):
    """轮播图模型"""
    # 字段
    title = models.CharField(max_length=500, verbose_name="广告标题")
    # upload_to 表示设置保存文件的子目录,系统会自动创建
    image = models.ImageField(upload_to="banner", null=True, blank=True, verbose_name="广告图片")
    link = models.CharField(max_length=255, null=True, blank=True, verbose_name="广告链接")
    is_http = models.BooleanField(default=False, verbose_name="是否是站外链接")
    remark = models.TextField(verbose_name="备注信息")
    is_show = models.BooleanField(default=False, verbose_name="是否显示")
    orders = models.IntegerField(default=1, verbose_name="排序")
    is_deleted = models.BooleanField(default=False, verbose_name="是否删除")
    # 表信息
    class Meta:
        db_table = "ly_banner"
        verbose_name = "广告轮播"
        verbose_name_plural = verbose_name

    # 自定义方法和自定义字段
    def __str__(self):
        return self.title