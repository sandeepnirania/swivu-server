from django.contrib import admin

from . import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
  list_display = (
      "id",
      "is_plan",
      "start_time",
      "end_time",
      "task",
  )
