from rest_framework import serializers

from . import models


class EventSerializer(serializers.ModelSerializer):

  class Meta:
    model = models.Event
    fields = (
        "id",
        "board",
        "task",
        "start_time",
        "end_time",
    )
    extra_kwargs = {"board": {"write_only": True}}
