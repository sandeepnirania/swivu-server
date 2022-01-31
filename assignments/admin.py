from django.contrib import admin

from . import models


@admin.register(models.Assignment)
class AssignmentAdmin(admin.ModelAdmin):
  list_display = (
      "id",
      "resource",
      "event",
  )
