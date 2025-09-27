from django.http import JsonResponse
from drf_spectacular.utils import extend_schema
from rest_framework import views, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Mission
from .serializers import MissionSerializer, MissionCatUpdateSerializer


class ListCreateMissionAPIView(views.APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=MissionSerializer,
        responses={200: MissionSerializer},
        methods=["POST"]
    )
    def post(self, request):
        data = request.data
        serializer = MissionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        responses={200: MissionSerializer(many=True)},
        methods=["GET"]
    )
    def get(self, request):
        missions = Mission.objects.all()
        serializer = MissionSerializer(missions, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class MissionDetailAPIView(views.APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        responses={200: MissionSerializer},
        methods=["GET"]
    )
    def get(self, request, mission_id):
        mission = get_object_or_404(Mission, id=mission_id)
        serializer = MissionSerializer(mission)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    @extend_schema(
        responses={204: None},
        methods=["DELETE"]
    )
    def delete(self, request, mission_id):
        mission = get_object_or_404(Mission, id=mission_id)

        if mission.cat is not None:
            return Response(
                data={"detail": "A mission cannot be deleted if it is already assigned to a cat"},
                status=status.HTTP_409_CONFLICT
            )

        mission.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class AssignMissionAPIView(views.APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=MissionCatUpdateSerializer,
        responses={200: None},
        methods=["POST"]
    )
    def post(self, request, mission_id):
        mission = get_object_or_404(Mission, id=mission_id)
        data = request.data
        serializer = MissionCatUpdateSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        cat = serializer.validated_data['cat']
        if mission.cat:
            return Response(
                data={"detail": "A cat has already been assigned to the mission."},
                status=status.HTTP_409_CONFLICT
            )
        if cat.missions.filter(complete=False).exists():
            return Response(
                data={"detail": f"The {cat.name} is on another mission."},
                status=status.HTTP_409_CONFLICT
            )
        mission.cat = cat
        mission.save()

        return Response(
            data={"detail": f"Mission {mission.id} assigned from {cat.name}"},
            status=status.HTTP_200_OK
        )


class UnassignMissionAPIView(views.APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=MissionCatUpdateSerializer,
        responses={200: None},
        methods=["POST"]
    )
    def post(self, request, mission_id):
        mission = get_object_or_404(Mission, id=mission_id)
        data = request.data
        serializer = MissionCatUpdateSerializer(data=data)
        if not serializer.is_valid():
            return JsonResponse(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        cat = serializer.validated_data['cat']

        if mission.cat is None:
            return Response(
                data={"detail": "There is no cat on this mission."},
                status=status.HTTP_404_NOT_FOUND
            )

        if mission.cat != cat:
            return Response(
                data={"detail": "The mission is assigned to another cat."},
                status=status.HTTP_409_CONFLICT
            )
        if mission.complete:
            return Response(
                data={"detail": f"Mission accomplished."},
                status=status.HTTP_409_CONFLICT
            )

        mission.cat = None
        mission.save()

        return Response(
            data={"detail": f"Mission {mission.id} unassigned from {cat.name}"},
            status=status.HTTP_200_OK
        )