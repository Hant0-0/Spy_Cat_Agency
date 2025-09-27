from django.urls import path

from .views import CatListCreateAPIView, CatDetailAPIView

urlpatterns = [
    path("", CatListCreateAPIView.as_view(), name="cats-list"),
    path("<int:cat_id>", CatDetailAPIView.as_view(), name="cat-detail")
]
