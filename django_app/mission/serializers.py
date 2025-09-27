from rest_framework import serializers

from .models import Mission
from target.models import Target

from cats.models import Cat

from target.serializers import TargetSerializer


class MissionSerializer(serializers.ModelSerializer):
    targets = TargetSerializer(many=True)

    class Meta:
        model = Mission
        fields = ["id", "cat", "complete", "targets"]

    def create(self, validated_data):
        targets = validated_data.pop("targets")
        cat = validated_data.get("cat")

        if cat and cat.missions.filter(complete=False).exists():
            raise serializers.ValidationError(f"{cat.name} alreadey have mission")

        mission = Mission.objects.create(**validated_data)
        target_objs = []
        if 1 > len(targets) or len(targets) > 3:
            raise serializers.ValidationError("The number of targets should be in the range from 1 to 3")

        for target in targets:
            target_objs.append(Target(
                **target,
                mission=mission
            ))

        Target.objects.bulk_create(target_objs)

        return mission


class MissionCatUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mission
        fields = ["cat"]


