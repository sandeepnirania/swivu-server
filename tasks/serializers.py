from rest_framework import serializers as framework_serializers

from . import models


class TaskSerializer(framework_serializers.ModelSerializer):

  class Meta:
    model = models.Task
    fields = (
        "id",
        "board",
        "display_name",
        "description",
    )
    extra_kwargs = {"board": {"write_only": True}}
