from django.contrib import admin
from . import models

# Register your models here.
class ProductCategory_admin(admin.ModelAdmin):
    pass

class ProductTag_admin(admin.ModelAdmin):
    pass

class Product_admin(admin.ModelAdmin):
    pass

class ProductDetails_admin(admin.ModelAdmin):
    pass

admin.site.register(models.ProductCategory_model, ProductCategory_admin)
admin.site.register(models.ProductTag_model, ProductTag_admin)
admin.site.register(models.Product_model, Product_admin)
admin.site.register(models.ProductDetails_model, ProductDetails_admin)
admin.site.register(models.ProductFeature_model)