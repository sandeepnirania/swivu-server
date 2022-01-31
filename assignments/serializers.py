from rest_framework import serializers as framework_serializers

from . import models


class AssignmentSerializer(framework_serializers.ModelSerializer):

  class Meta:
    model = models.Assignment
    fields = (
        "id",
        "board",
        "resource",
        "event",
    )
    extra_kwargs = {"board": {"write_only": True}}
