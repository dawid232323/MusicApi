from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from musicApiApp.models import Album
from musicApiApp.serializers import AlbumSerializer


class AlbumView(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    queryset = Album.objects.all()
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, album_id=None, *args, **kwargs):
        retrieved_object = self.queryset.get(pk=album_id)
        serialised_object = self.serializer_class(retrieved_object)
        return Response(serialised_object.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        seirlised_objects = self.serializer_class(self.queryset, many=True)
        return Response(seirlised_objects.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request_body = request.data
        serialized_body = self.serializer_class(data=request_body)
        serialized_body.is_valid(raise_exception=True)
        serialized_body.save()
        return Response(serialized_body.data, status=status.HTTP_201_CREATED)
