from rest_framework import viewsets, status
from rest_framework.response import Response

from musicApiApp.models import Genre
from musicApiApp.serializers import GenreSerializer


class GenreView(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def retrieve(self, request, genre_id=None, *args, **kwargs):
        retrieved_object = self.queryset.get(pk=genre_id)
        serialized_object = self.serializer_class(retrieved_object)
        return Response(serialized_object.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        serialized_objects = self.serializer_class(self.queryset, many=True)
        return Response(serialized_objects.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request_body = request.data
        serialized_body = self.serializer_class(data=request_body)
        serialized_body.is_valid(raise_exception=True)
        serialized_body.save()
        return Response(serialized_body.data, status=status.HTTP_201_CREATED)
