from django.urls import path

from .views import CatListCreateAPIView, CatDetailAPIView

urlpatterns = [
    path("", CatListCreateAPIView.as_view()),
    path("<int:cat_id>", CatDetailAPIView.as_view())
]
