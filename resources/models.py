from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from boards.models import BoardScopedModelMixin


class ResourceType():
  PERSON = 1
  EQUIPMENT = 2
  VEHICLE = 3
  CHOICES = (
      (PERSON, "Person"),
      (EQUIPMENT, "Equipment"),
      (VEHICLE, "Vehicle"),
  )
  DEFAULT = PERSON


class Resource(BoardScopedModelMixin):

  class Meta:
    verbose_name = "resource"

  # A resource may be a person, a piece of equipment, or a vehicle.
  type = models.PositiveIntegerField(
      blank=False,
      choices=ResourceType.CHOICES,
      default=ResourceType.DEFAULT,
      null=False,
      verbose_name=_("resource type"),
  )

  # An optional icon or avatar.
  image_url = models.URLField(
      blank=True,
      null=True,
      max_length=200,
      verbose_name=_("image url"),
  )

  # The name to appear in the Resource Grid.
  display_name = models.TextField(
      blank=False,
      null=False,
      db_index=True,
      verbose_name=_("display name"),
  )

  # The name to appear in the Resource Grid.
  display_name = models.TextField(
      blank=False,
      null=False,
      db_index=True,
      verbose_name=_("display name"),
  )

  # Descriptive text.
  description = models.TextField(
      blank=True,
      null=True,
      verbose_name=_("description"),
  )

  # A Resource may be associated with a User.  (However, it is not required that every person have a user.)
  user = models.ForeignKey(
      to=get_user_model(),
      blank=True,
      null=True,
      on_delete=models.SET_NULL,
      verbose_name=_("user"),
  )
