from rest_framework import serializers as framework_serializers

from . import models


class EventSerializer(framework_serializers.ModelSerializer):

  class Meta:
    model = models.Event
    fields = (
        "id",
        "is_plan",
        "start_time",
        "duration_hours",
        "resource_id",
        "task_id",
    )
