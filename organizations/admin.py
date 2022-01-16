from django.contrib import admin

from . import models


@admin.register(models.Organization)
class TaskAdmin(admin.ModelAdmin):
  list_display = ("id", "name")
