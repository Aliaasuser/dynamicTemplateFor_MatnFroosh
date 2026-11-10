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

class UserGroup_model(models.Model):
    title = models.CharField(verbose_name='نام گروه بندی', max_length=75, unique=True)

    def __str__(self):
        return f'گروه ({self.title})'

    class Meta:
        verbose_name = 'گروه کاربری'
        verbose_name_plural = 'گروه های کاربری'

from django.conf import settings

class UserConnectorToUserGroup(models.Model):
    alias = models.CharField(verbose_name='نام مستعار', max_length=75, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='کاربر', on_delete=models.CASCADE, related_name='group_connectors')
    user_group = models.ForeignKey(UserGroup_model, verbose_name='گروه کاربری', on_delete=models.CASCADE, related_name='user_connectors')

    def save(self, *args, **kwargs):
        if self.alias is None:
            self.alias = self.user.username
        if UserConnectorToUserGroup.objects.filter(models.Q(user=self.user) | models.Q(alias=self.alias), user_group=self.user_group):
            raise 'Duplicate user or alias in the user group! If you have already added this user to the group, you must use the existing connection. If you have not added them to the group, then you have chosen a duplicate alias; you must select a new one.'
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.alias} in ({self.user_group.title})'

    class Meta:
        verbose_name = 'رابط گروه کاربری'
        verbose_name_plural = 'رابط های گروه های کاربری'