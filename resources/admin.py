from django.contrib import admin

from . import models


@admin.register(models.Resource)
class ResourceAdmin(admin.ModelAdmin):
  list_display = (
      "id",
      "display_name",
      "description",
  )
