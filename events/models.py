from django.db import models
from django.utils.translation import gettext_lazy as _

from boards.models import BoardScopedModelMixin


class Event(BoardScopedModelMixin):

  class Meta:
    verbose_name = "event"

  is_plan = models.BooleanField(blank=False, null=False, default=False, db_index=True)

  start_time = models.DateTimeField(blank=False, null=False, db_index=True)

  duration_hours = models.PositiveIntegerField(blank=False, null=False, default=24)

  resource = models.ForeignKey(to="resources.Resource",
                               blank=False,
                               null=False,
                               db_index=True,
                               on_delete=models.CASCADE)

  task = models.ForeignKey(to="tasks.Task",
                           blank=False,
                           null=False,
                           db_index=True,
                           on_delete=models.CASCADE)

  def to_json(self):
    json = {"start_time": self.start_time.strftime("Y-m-d H:M")}
    json.update({
        key: getattr(self, key)
        for key in ("id", "is_plan", "duration_hours", "resource_id", "task_id")
    })
    return json
