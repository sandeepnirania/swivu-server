from django.contrib import admin

from . import models


@admin.register(models.Revision)
class RevisionAdmin(admin.ModelAdmin):
  list_display = (
      "id",
      "board",
      "created_at",
  )
