from django.contrib import admin
from . import models

# Register your models here.
class HML_admin(admin.ModelAdmin):
    pass

admin.site.register(models.HeaderMainLinks_model, HML_admin)