from drf_spectacular.utils import extend_schema
from rest_framework import views, status, generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Cat

from .serializers import CatSerializer

from .fillters import FilAvailableCatFilter

class CatListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    filter_backends = [FilAvailableCatFilter]


class CatDetailAPIView(views.APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        responses={200: CatSerializer},
        methods=["GET"]
    )
    def get(self, request, cat_id):
        cat = get_object_or_404(Cat, id=cat_id)
        serializer = CatSerializer(cat)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )


    @extend_schema(
        request=CatSerializer,
        responses={200: CatSerializer},
        methods=["PATCH"]
    )
    def patch(self, request, cat_id):
        cat = get_object_or_404(Cat, id=cat_id)
        data = request.data
        serializer = CatSerializer(instance=cat, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @extend_schema(
        responses={204: None},
        methods=["DELETE"]
    )
    def delete(self, request, cat_id):
        cat = get_object_or_404(Cat, id=cat_id)

        if cat.missions.filter(complete=False).exists():
            return Response(
                data={"detail": "You cannot delete a cat while it is on a mission"},
                status=status.HTTP_409_CONFLICT
            )

        cat.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
