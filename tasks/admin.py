from django.contrib import admin

from . import models


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
  list_display = (
      "id",
      "display_name",
      "description",
  )
