from collections.abc import Callable
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
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

    SONGS_RELATED_FIELD = 'songs'

    def retrieve(self, request, album_id=None, *args, **kwargs):
        should_show_songs = self._should_process_songs(request.query_params)
        callback_getter: Callable([int], AlbumSerializer)
        if should_show_songs:
            callback_getter = self._get_album_with_songs
        else:
            callback_getter = self._get_serialised_album_only
        try:
            serialised_object = callback_getter(album_id)
        except ObjectDoesNotExist:
            return self._get_album_does_not_exist_response()
        return Response(serialised_object.data, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        should_show_songs = self._should_process_songs(request.query_params)
        get_albums_callback = Callable([], AlbumSerializer)
        if should_show_songs:
            get_albums_callback = self._get_serialised_albums_with_songs
        else:
            get_albums_callback = self._get_serialised_albums_only
        serialised_objects = get_albums_callback()
        return Response(serialised_objects.data, status=status.HTTP_200_OK)

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

    def update(self, request, album_id=None, *args, **kwargs):
        if album_id is None:
            return get_error_response(error_message='Album id should be specified',
                                      response_status=status.HTTP_400_BAD_REQUEST)
        request_body = request.data
        try:
            updated_object = self.queryset.get(pk=album_id)
        except ObjectDoesNotExist:
            return self._get_album_does_not_exist_response()
        serialized_object = self.serializer_class(updated_object, data=request_body, partial=True)
        serialized_object.is_valid(raise_exception=True)
        serialized_object.save()
        return Response(serialized_object.data, status=status.HTTP_200_OK)

    def destroy(self, request, album_id=None, *args, **kwargs):
        try:
            album_to_delete = self.queryset.get(pk=album_id)
        except ObjectDoesNotExist:
            return self._get_album_does_not_exist_response()
        album_to_delete.delete()
        return Response(status=status.HTTP_200_OK)

    def _get_album_with_songs(self, album_id: int) -> AlbumSongsSerializer:
        album_with_details = self.queryset.prefetch_related(self.SONGS_RELATED_FIELD).get(pk=album_id)
        serialized_album = self.secondary_serializer_class(instance=album_with_details)
        return serialized_album

    def _get_serialised_albums_with_songs(self) -> AlbumSongsSerializer:
        all_albums = self.queryset.prefetch_related(self.SONGS_RELATED_FIELD).all()
        serialised_all_albums = self.secondary_serializer_class(all_albums, many=True)
        return serialised_all_albums

    def _get_serialised_albums_only(self) -> AlbumSerializer:
        return self.serializer_class(self.queryset, many=True)

    def _get_serialised_album_only(self, album_id: int) -> AlbumSerializer:
        album_only = self.queryset.get(pk=album_id)
        return self.serializer_class(album_only)

    def _should_process_songs(self, query_params) -> bool:
        return query_params.get('songs') == 'True'

    def _get_serialized_songs_request(self, request_body) -> AlbumSongsSerializer:
        return self.secondary_serializer_class(data=request_body)

    def _get_serialized_album_only_request(self, request_body) -> AlbumSerializer:
        return self.serializer_class(data=request_body)

    def _get_album_does_not_exist_response(self) -> JsonResponse:
        return get_error_response(error_message='Album with given id does not exist',
                                  response_status=status.HTTP_400_BAD_REQUEST)
