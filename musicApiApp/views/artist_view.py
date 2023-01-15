from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from musicApiApp.models import Artist
from musicApiApp.serializers import ArtistSerializer
from musicApiApp.utils.error_utils import get_error_response


class ArtistView(viewsets.ModelViewSet):
    serializer_class = ArtistSerializer
    queryset = Artist.objects.all()
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, artist_id=None, *args, **kwargs):
        try:
            retrieved_object = self.queryset.get(pk=artist_id)
        except ObjectDoesNotExist:
            return self._get_artist_does_not_exist_response()
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

    def update(self, request, artist_id=None, *args, **kwargs):
        request_body = request.data
        try:
            updated_object = self.queryset.get(pk=artist_id)
        except ObjectDoesNotExist:
            return self._get_artist_does_not_exist_response()
        serialized_object = self.serializer_class(updated_object, data=request_body, partial=True)
        serialized_object.is_valid(raise_exception=True)
        serialized_object.save()
        return Response(serialized_object.data, status=status.HTTP_200_OK)

    def destroy(self, request, artist_id=None, *args, **kwargs):
        try:
            artist_to_delete = self.queryset.get(pk=artist_id)
        except ObjectDoesNotExist:
            return self._get_artist_does_not_exist_response()
        artist_to_delete.delete()
        return Response(status=status.HTTP_200_OK)

    def _get_artist_does_not_exist_response(self):
        return get_error_response(error_message='Artist with given id does not exist',
                                       response_status=status.HTTP_400_BAD_REQUEST)
