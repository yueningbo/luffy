from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
	'''自定义用户'''
	mobile = models.CharField(max_length=15, verbose_name="手机号码")
	avatar = models.ImageField(upload_to="avatar", null=True, blank=True, verbose_name="用户头像")
	wechat = models.CharField(max_length=50, null=True, blank=True, verbose_name="微信号")


	class Meta:
		db_table = 'ly_user'
		verbose_name = "用户信息"
		verbose_name_plural = verbose_name
	
	def __str__(self):
		return self.username


