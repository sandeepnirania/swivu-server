from django.db import models
from django.utils.translation import gettext_lazy as _

from boards.models import BoardScopedModelMixin


class Assignment(BoardScopedModelMixin):

  class Meta:
    verbose_name = "assignment"

  resource = models.ForeignKey(to="resources.Resource",
                               blank=False,
                               null=False,
                               db_index=True,
                               on_delete=models.CASCADE)

  event = models.ForeignKey(to="events.Event",
                            blank=False,
                            null=False,
                            db_index=True,
                            on_delete=models.CASCADE)
