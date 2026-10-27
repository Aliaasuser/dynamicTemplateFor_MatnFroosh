from django.db import models

# Create your models here.
class HeaderMainLinks_model(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=50)
    url_name = models.CharField(verbose_name='اسم پیوند', max_length=100, null=True, blank=True)
    url = models.URLField(verbose_name='آدرس پیوند', max_length=300, null=True, blank=True)
    father = models.ForeignKey('HeaderMainLinks_model', verbose_name='لینک والد', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(verbose_name='قابلت نمایش', default=True)

    def __str__(self):
        return f'[{self.title}]({'داخلی' if self.url_name != None else 'خارجی'})'

    class Meta:
        verbose_name = 'پیوند اصلی سربرگ'
        verbose_name_plural = 'پیوندهای اصلی سربرگ'