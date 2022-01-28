from rest_framework import serializers as framework_serializers

from . import models


class ResourceSerializer(framework_serializers.ModelSerializer):

  class Meta:
    model = models.Resource
    fields = (
        "id",
        "type",
        "image_url",
        "display_name",
        "description",
        "user_id",
    )
