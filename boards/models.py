from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Board(models.Model):
  # A board is the parent of collections of resources and tasks, and of the events that link
  # elements of the other two.

  class Meta:
    verbose_name = "board"

  # Human-readable name for this board.
  display_name = models.TextField(blank=False, null=False)

  # URL-friendly name for this board.
  slug = models.TextField(blank=False, null=False, db_index=True)

  # The user who created this board.
  creator = models.ForeignKey(
      blank=False,
      null=True,  # for SET_NULL.
      on_delete=models.SET_NULL,
      to=get_user_model(),
      verbose_name=_("creator"),
  )

  # The organization this Board is associated with.  May be null.
  organization = models.ForeignKey(
      blank=False,
      null=True,
      on_delete=models.SET_NULL,
      to="organizations.Organization",
      verbose_name=_("organization"),
  )

  def __str__(self):
    return self.display_name


class BoardScopedModelMixin(models.Model):
  """
    Abstract base class for a model type that is a child of a Board.
  """

  class Meta:
    abstract = True

  board = models.ForeignKey(
      blank=False,
      db_index=True,
      null=False,
      on_delete=models.CASCADE,
      related_name="%(app_label)s_%(class)ss",
      to=Board,
      verbose_name=_("business"),
  )
