from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from boards.models import BoardScopedModelMixin


class Resource(BoardScopedModelMixin):

  class Meta:
    verbose_name = "resource"

  image_url = models.URLField(blank=True, null=True, max_length=200)

  display_name = models.TextField(blank=False, null=False, db_index=True)

  description = models.TextField(blank=True, null=True)

  # A Resource may be associated with a User.
  user = models.ForeignKey(to=get_user_model(), blank=True, null=True, on_delete=models.SET_NULL)

  def to_json(self):
    return {
        key: getattr(self, key)
        for key in ("id", "image_url", "display_name", "description", "user_id")
    }
