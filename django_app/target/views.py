from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status, views
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from mission.models import Mission
from rest_framework.status import HTTP_200_OK

from .models import Target
from .serializers import TargetSerializer, UpdateNotesTargetSerializer


class TargetDetailAPIView(views.APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        responses={200: TargetSerializer},
        methods=["GET"]
    )
    def get(self, request, mission_id, target_id):
        try:
            target = Target.objects.select_related('mission').get(mission__id=mission_id, id=target_id)
        except ObjectDoesNotExist:
            return Response(
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = TargetSerializer(target)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    @extend_schema(
        request=UpdateNotesTargetSerializer,
        responses={200: UpdateNotesTargetSerializer},
        methods=["PATCH"]
    )
    def patch(self, request, mission_id, target_id):
        try:
            target = Target.objects.select_related("mission").get(mission__id=mission_id, id=target_id)
        except ObjectDoesNotExist:
            return Response(
                data={"detail": "Target does not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        if target.mission.complete or target.complete:
            return Response(
                data={"detail": "Notes cannot be changed if the target or mission has already been completed."},
                status=status.HTTP_409_CONFLICT
            )

        data = request.data
        serializer = UpdateNotesTargetSerializer(target, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )





class TargetCompleteAPIView(views.APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        responses={200: None},
        methods=["POST"]
    )
    def post(self, request, mission_id, target_id):

        try:
            with (transaction.atomic()):
                target = Target.objects.select_for_update(
                ).select_related("mission").get(mission__id=mission_id, id=target_id)

                if target.complete:
                    return Response(
                        data={"detail": "Target has already completed"},
                        status=status.HTTP_409_CONFLICT
                    )

                target.complete = True
                target.save()

                mission = target.mission
                total_targets = mission.targets.count()
                total_complete_targets = mission.targets.filter(complete=True).count()

                if total_complete_targets == total_targets:
                    target.mission.complete = True

                    target.mission.save()

                return Response(
                    data={"detail": "Target completed successful"},
                    status=HTTP_200_OK
                )

        except Target.DoesNotExist:
            return Response(
                data={"detail": "Target does not found"},
                status=status.HTTP_404_NOT_FOUND
            )

