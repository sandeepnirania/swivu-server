from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class Organization(models.Model):
  name = models.TextField(blank=False, null=False, db_index=True)

  # members = models.ManyToManyField(to=get_user_model())
