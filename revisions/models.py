from django.db import models
from django.utils.translation import gettext_lazy as _

from boards.models import BoardScopedModelMixin


class Revision(BoardScopedModelMixin):
  # Maintains revision history across a Board.  The automatic id field serves as the
  # ascending sequence of revi required Bryntum sync protocol depends on ascending
  # revision ids.

  # Timestamp for this revision.
  created_at = models.DateTimeField(
      auto_now_add=True,
      db_index=True,
      editable=False,
      verbose_name=_("created at"),
  )

  # Details of the revision. Format:
  # .events, .resources, .tasks
  diff = models.JSONField(blank=False, null=False)
