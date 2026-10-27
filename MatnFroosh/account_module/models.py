from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    avatar = models.ImageField(verbose_name='تصویر پروفایل', null=True, blank=True)
    email_active_code = models.CharField(verbose_name='کد فعال سازی حساب کاربری', max_length=100, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='فعال بودن کاربر', default=False)
    level = models.CharField(verbose_name='سطح کاربری', max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربرها'