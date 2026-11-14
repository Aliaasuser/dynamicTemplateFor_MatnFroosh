from django.db import models
from django.conf import settings
from product_module.models import Product_model
from my_template_tags.templatetags import my_filters

# Create your models here.

class CommentForProduct_model(models.Model):
    product = models.ForeignKey(Product_model, verbose_name='محصول هدف', on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='کاربر', on_delete=models.CASCADE, related_name='products_comments')
    text = models.TextField(verbose_name='متن نظر/پیشنهاد', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='فعال بودن', default=True)
    is_deleted = models.BooleanField(verbose_name='حذف شده', default=False)
    has_report = models.BooleanField(verbose_name='دارای گزارش', default=False)
    report = models.CharField(verbose_name='متن گزارش', max_length=100, null=True, blank=True)
    father = models.ForeignKey('CommentForProduct_model', verbose_name='در پاسخ به', on_delete=models.PROTECT, null=True, blank=True, related_name='children')

    def __str__(self):
        return f'for({self.product.title})from({self.user.get_full_name()}) "{my_filters.limitText(self.text, 6)}"'

    class Meta:
        verbose_name = 'نظر/پیشنهاد برای کالا'
        verbose_name_plural = 'نظرها/پیشنهادها برای کالاها'

class ScoreForProduct_model(models.Model):
    product = models.ForeignKey(Product_model, verbose_name='محصول هدف', on_delete=models.CASCADE, related_name='scores')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='کاربر', on_delete=models.CASCADE, related_name='products_scores')
    comment = models.OneToOneField(CommentForProduct_model, verbose_name='نظر/پیشنهاد', on_delete=models.CASCADE, related_name='score')
    value = models.IntegerField(verbose_name='مقدار', default=0)

    def __str__(self):
        return f'[{self.product.title}][{self.user.get_full_name()}] : ({self.value})'

    def save(self, *args, **kwargs):
        temp = ScoreForProduct_model.objects.filter(product=self.product, user=self.user).exclude(pk=self.pk).last()
        if temp:
            temp.comment = self.comment
            temp.value = self.value
            temp.save()
        else:
            super().save(*args, **kwargs)
        temp = Product_model.objects.filter(pk=self.product.pk).last()
        temp.rating = round(ScoreForProduct_model.objects.filter(product=self.product).aggregate(models.Avg('value')).get('value__avg'), 1)
        temp.save()
        return

    class Meta:
        verbose_name = 'امتیاز کالا'
        verbose_name_plural = 'امتیازهای کالاها'
