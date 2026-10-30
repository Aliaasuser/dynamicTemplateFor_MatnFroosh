from django.db import models

# Create your models here.
class HeaderMainLinks_model(models.Model):
    text = models.CharField(verbose_name='متن پیوند', max_length=50, default='پیوند')
    title = models.CharField(verbose_name='عنوان پیوند', max_length=50, null=True, blank=True)
    url_name = models.CharField(verbose_name='اسم پیوند', max_length=100, null=True, blank=True)
    url = models.URLField(verbose_name='آدرس پیوند', max_length=300, null=True, blank=True)
    father = models.ForeignKey('HeaderMainLinks_model', verbose_name='شیء والد', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='قابلت نمایش', default=True)

    def __str__(self):
        return f'[{self.text}]({'داخلی' if self.url_name != None else 'خارجی' if self.url != None else ''})'

    class Meta:
        verbose_name = 'پیوند اصلی سربرگ'
        verbose_name_plural = 'پیوندهای اصلی سربرگ'

class HeaderLogo_model(models.Model):
    image = models.ImageField(verbose_name='تصویر لوگو', upload_to='admin/logo/')
    title = models.CharField(verbose_name='عنوان لوگو', max_length=75, null=True, blank=True)
    alt = models.CharField(verbose_name='متن جایگزین', max_length=75, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='فعال بودن لوگو', default=True)

    def __str__(self):
        return f'({ self.title })'

    def save(self, *args, **kwargs):
        if self.is_active:
            other_active_objs = HeaderLogo_model.objects.exclude(pk=self.pk).filter(is_active=True)
            for obj in other_active_objs:
                obj.is_active = False
                obj.save()
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'لوگو'
        verbose_name_plural = 'لوگوها'

class HeaderNavbarLinks_model(models.Model):
    text = models.CharField(verbose_name='متن پیوند', max_length=50, default='پیوند')
    url_name = models.CharField(verbose_name='اسم پیوند', max_length=100, null=True, blank=True)
    url = models.URLField(verbose_name='آدرس پیوند', max_length=300, null=True, blank=True)
    more_classes = models.CharField(verbose_name='کلاس های css بیشتر', max_length=300, null=True, blank=True)
    father = models.ForeignKey('HeaderNavbarLinks_model', verbose_name='شیء والد', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='قابلت نمایش', default=True)

    def __str__(self):
        return f'[{self.text}]({'داخلی' if self.url_name != None else 'خارجی' if self.url != None else ''})'

    class Meta:
        verbose_name = 'پیوند داخل نوار ناوبری'
        verbose_name_plural = 'پیوندهای نوار ناوبری'