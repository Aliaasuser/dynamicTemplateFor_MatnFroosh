from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.CommentForProduct_model)
admin.site.register(models.ScoreForProduct_model)