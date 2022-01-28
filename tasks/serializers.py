from rest_framework import serializers as framework_serializers

from . import models


class TaskSerializer(framework_serializers.ModelSerializer):

  class Meta:
    model = models.Task
    fields = (
        "id",
        "display_name",
        "description",
    )
