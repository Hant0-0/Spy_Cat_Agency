from django.urls import path

from .views import (ListCreateMissionAPIView, MissionDetailAPIView,
                    AssignMissionAPIView, UnassignMissionAPIView)

from target.views import TargetDetailAPIView, TargetCompleteAPIView

urlpatterns = [
    path("", ListCreateMissionAPIView.as_view()),
    path("<int:mission_id>", MissionDetailAPIView.as_view()),
    path("<int:mission_id>/assign/", AssignMissionAPIView.as_view()),
    path("<int:mission_id>/unassign/", UnassignMissionAPIView.as_view()),

    #TARGET
    path("<int:mission_id>/targets/<int:target_id>/", TargetDetailAPIView.as_view()),
    path("<int:mission_id>/targets/<int:target_id>/complete/", TargetCompleteAPIView.as_view()),
]