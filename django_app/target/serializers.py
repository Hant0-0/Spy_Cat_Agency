import pycountry
from rest_framework import serializers

from target.models import Target


class TargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ["name", "country", "notes", "complete"]

    def validate_country(self, value):
        if not pycountry.countries.get(name=value):
            raise serializers.ValidationError(f"{value} is not valid country")
        return value


class UpdateNotesTargetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Target
        fields = ["notes"]