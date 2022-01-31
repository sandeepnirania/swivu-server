from django.db import models
from django.utils.translation import gettext_lazy as _

from boards.models import BoardScopedModelMixin


class Event(BoardScopedModelMixin):

  class Meta:
    verbose_name = "event"

  is_plan = models.BooleanField(blank=False, null=False, default=False, db_index=True)

  start_time = models.DateTimeField(blank=False, null=False, db_index=True)

  end_time = models.DateTimeField(blank=False, null=False, db_index=False)

  task = models.ForeignKey(to="tasks.Task",
                           blank=False,
                           null=False,
                           db_index=True,
                           on_delete=models.CASCADE)
