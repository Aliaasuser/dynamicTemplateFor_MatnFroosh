from django.db import models
from django.db.models import Q
from django.utils.text import slugify
from django.utils import timezone
from django.conf import settings

# Create your models here.
class ProductCategory_model(models.Model):
    title = models.CharField(verbose_name='عنوان دسته بندی', max_length=75, unique=True)
    is_active = models.BooleanField(verbose_name='فعال بودن', default=True)
    father = models.ForeignKey('ProductCategory_model', verbose_name='والد', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی محصولات'
        verbose_name_plural = 'دسته بندی های محصولات'

class ProductTag_model(models.Model):
    title = models.CharField(verbose_name='عنوان برچسب', max_length=75, unique=True)
    is_active = models.BooleanField(verbose_name='فعال بودن', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'برچسب محصولات'
        verbose_name_plural = 'برچسب های محصولات'

class Product_model(models.Model):
    title = models.CharField(verbose_name='عنوان محصول', max_length=100, unique=True)
    slug = models.SlugField(verbose_name='slug', max_length=150, unique=True, default='', editable=False, allow_unicode=True)
    price = models.IntegerField(verbose_name='قیمت(به تومان)')
    is_active = models.BooleanField(verbose_name='فعال بودن', default=True)
    is_deleted = models.BooleanField(verbose_name='حذف شده', default=False)
    rating = models.FloatField(verbose_name='امتیاز از پنج', default=0)
    image = models.ImageField(verbose_name='تصویر اصلی محصول', upload_to='products/main_image', null=True, blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='مالک محصول', on_delete=models.CASCADE, related_name='products')
    short_description = models.CharField(verbose_name='توضیحات کوتاه', max_length=700, null=True, blank=True)
    categories = models.ManyToManyField(ProductCategory_model, verbose_name='دسته بندی ها', blank=True, related_name='products')
    tags = models.ManyToManyField(ProductTag_model, verbose_name='برچسب ها', blank=True, related_name='products')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'محصول متنی'
        verbose_name_plural = 'محصولات متنی'

class ProductFeature_model(models.Model):
    title = models.CharField(verbose_name='عنوان ویژگی', max_length=150, unique=True)
    is_active = models.BooleanField(verbose_name='فعال بودن', default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'ویژگی کالا'
        verbose_name_plural = 'ویژگی های کالاها'

class ProductDetails_model(models.Model):
    image1 = models.ImageField(verbose_name='تصویر اول محصول', upload_to='products/secondary_image/', null=True, blank=True)
    image2 = models.ImageField(verbose_name='تصویر دوم محصول', upload_to='products/secondary_image/', null=True, blank=True)
    image3 = models.ImageField(verbose_name='تصویر سوم محصول', upload_to='products/secondary_image/', null=True, blank=True)
    creation_date = models.DateField(verbose_name='تاریخ ایجاد محصول', auto_now_add=True)
    last_update = models.DateTimeField(verbose_name='آخرین بروزرسانی', default=timezone.now())
    creators = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='سازندگان/طراحان محصول', blank=True, related_name='created_products')
    product = models.OneToOneField(Product_model, verbose_name='محصول مرتبط', on_delete=models.CASCADE, related_name='details')
    has_preview = models.BooleanField(verbose_name='دارای پیش نمایش', default=False)
    buyers = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='خریداران محصول', blank=True, related_name='buyed_products')
    num_of_sales = models.IntegerField(verbose_name='تعداد فروش', default=0)
    long_description = models.TextField(verbose_name='توضیحات کامل', null=True, blank=True)
    with_features = models.ManyToManyField(ProductFeature_model, verbose_name='دارای ویژگی های', blank=True, related_name='pd_with_these')
    without_features = models.ManyToManyField(ProductFeature_model, verbose_name='بدون ویژگی های', blank=True, related_name='pd_without_these')

    def __str__(self):
        return f'details for ({self.product.title})'

    def save(self, *args, **kwargs):
        if self.image2 and not self.image1 and not self.image3:
            self.image1 = self.image2
            self.image2 = None
        elif self.image3 and not self.image1 and not self.image2:
            self.image1 = self.image3
            self.image3 = None
        elif self.image2 and self.image3 and not self.image1:
            self.image1 = self.image2
            self.image2 = self.image3
            self.image3 = None
        elif self.image1 and self.image3 and not self.image2:
            self.image2 = self.image3
            self.image3 = None
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'جزئیات محصول'
        verbose_name_plural = 'جزئیات محصولات'