from django.db import models
from django.utils.translation import gettext_lazy as _

from boards.models import BoardScopedModelMixin


class Task(BoardScopedModelMixin):

  class Meta:
    verbose_name = "task"

  display_name = models.TextField(blank=False, null=False)

  description = models.TextField(blank=True, null=True)

  def to_json(self):
    return {key: getattr(self, key) for key in ("id", "display_name", "description")}
