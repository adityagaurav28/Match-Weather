from django.contrib import admin

from . import models

# Register your models here.
admin.site.register(models.Match_Detail)
admin.site.register(models.Series_Detail)
admin.site.register(models.Dates_Detail)
admin.site.register(models.UpdateDataTime)