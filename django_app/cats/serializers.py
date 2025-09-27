import requests
from rest_framework import serializers
from django.core.cache import cache

from .models import Cat


class CatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cat
        fields = "__all__"

    def validate_breed(self, value):
        data = cache.get(value)
        if data is None:
            response = requests.get(url=f"https://api.thecatapi.com/v1/breeds/search?q={value}")
            if response.status_code != 200:
                raise serializers.ValidationError("Cannot validate breed: API error")
            breed_data = response.json()
            if not breed_data:
                raise serializers.ValidationError("This breed does not exist")

            cache.set(value, breed_data[0])

        return value

    def update(self, instance, validated_data):
        allowed_fields = ["salary"]
        for field in validated_data:
            if field in allowed_fields:
                setattr(instance, field, validated_data[field])

        instance.save()
        return instance
