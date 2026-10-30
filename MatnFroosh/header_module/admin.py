from django.contrib import admin
from . import models

# Register your models here.
class HeaderMainLinks_admin(admin.ModelAdmin):
    pass

class HeaderLogo_admin(admin.ModelAdmin):
    pass

class HeaderNavbarLinks_admin(admin.ModelAdmin):
    pass

admin.site.register(models.HeaderMainLinks_model, HeaderMainLinks_admin)
admin.site.register(models.HeaderLogo_model, HeaderLogo_admin)
admin.site.register(models.HeaderNavbarLinks_model, HeaderNavbarLinks_admin)