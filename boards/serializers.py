from rest_framework import serializers as framework_serializers

from . import models


class BoardSerializer(framework_serializers.ModelSerializer):

  class Meta:
    model = models.Board
    fields = (
        "id",
        "display_name",
        "slug",
        "creator",
        "organization",
    )
