from rest_framework import serializers as framework_serializers

from . import models


class ResourceSerializer(framework_serializers.ModelSerializer):

  class Meta:
    model = models.Resource
    fields = (
        "id",
        "board",
        "type",
        "image_url",
        "display_name",
        "description",
        "user",
    )
    extra_kwargs = {"board": {"write_only": True}}
