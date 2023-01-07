from collections.abc import Callable
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from musicApiApp.models import Album
from musicApiApp.serializers import AlbumSerializer, AlbumSongsSerializer
from musicApiApp.utils.error_utils import get_error_response


class AlbumView(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    secondary_serializer_class = AlbumSongsSerializer
    queryset = Album.objects.all()
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, album_id=None, *args, **kwargs):
        should_show_songs = self._should_process_songs(request.query_params)
        callback_getter: Callable([int], AlbumSerializer)
        if should_show_songs:
            callback_getter = self._get_album_with_songs
        else:
            callback_getter = self._get_album_only
        try:
            serialised_object = callback_getter(album_id)
        except ObjectDoesNotExist:
            return get_error_response(error_message='Album with given id does not exist',
                                      response_status=status.HTTP_400_BAD_REQUEST)
        return Response(serialised_object.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        seirlised_objects = self.serializer_class(self.queryset, many=True)
        return Response(seirlised_objects.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        should_save_with_songs = self._should_process_songs(request.query_params)
        request_body = request.data
        serialized_body_callback: Callable([dict], AlbumSerializer)
        if should_save_with_songs:
            serialized_body_callback = self._get_serialized_songs_request
        else:
            serialized_body_callback = self._get_serialized_album_only_request
        serialized_body = serialized_body_callback(request_body)
        serialized_body.is_valid(raise_exception=True)
        serialized_body.save()
        return Response(serialized_body.data, status=status.HTTP_201_CREATED)

    def _get_album_with_songs(self, album_id: int):
        album_with_details = self.queryset.prefetch_related('songs').get(pk=album_id)
        serialized_album = self.secondary_serializer_class(instance=album_with_details)
        return serialized_album

    def _get_album_only(self, album_id: int):
        album_only = self.queryset.get(pk=album_id)
        return self.serializer_class(album_only)

    def _should_process_songs(self, query_params):
        return query_params.get('songs') == 'True'

    def _get_serialized_songs_request(self, request_body) -> AlbumSongsSerializer:
        return self.secondary_serializer_class(data=request_body)

    def _get_serialized_album_only_request(self, request_body) -> AlbumSerializer:
        return self.serializer_class(data=request_body)
