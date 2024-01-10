from rest_framework import serializers

from .models import RegionModel


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionModel
        fields = "__all__"
