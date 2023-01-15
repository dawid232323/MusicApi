from collections.abc import Callable
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from musicApiApp.models import Artist
from musicApiApp.serializers import ArtistSerializer
from musicApiApp.serializers.artist_serializer import DisplayAlbumsArtistSerializer
from musicApiApp.utils.error_utils import get_error_response


class ArtistView(viewsets.ModelViewSet):
    serializer_class = ArtistSerializer
    secondary_display_serializer = DisplayAlbumsArtistSerializer
    queryset = Artist.objects.all()
    permission_classes = (IsAuthenticated,)

    ALBUMS_RELATED_FIELD = 'albums'

    def retrieve(self, request, artist_id=None, *args, **kwargs):
        should_show_albums = self._should_process_albums(request.query_params)
        callback_getter: Callable([int], ArtistSerializer)
        if should_show_albums:
            callback_getter = self._get_artist_with_albums
        else:
            callback_getter = self._get_serialized_artist_only
        try:
            serialized_object = callback_getter(artist_id)
        except ObjectDoesNotExist:
            return self._get_artist_does_not_exist_response()
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

    def _should_process_albums(self, query_params) -> bool:
        return query_params.get('albums') == 'True'

    def _get_artist_with_albums(self, artist_id: int) -> DisplayAlbumsArtistSerializer:
        artist_with_details = self.queryset.prefetch_related(self.ALBUMS_RELATED_FIELD).get(pk=artist_id)
        serialized_artist = self.secondary_display_serializer(instance=artist_with_details)
        return serialized_artist

    def _get_serialized_artist_only(self, artist_id: int) -> ArtistSerializer:
        artist_only = self.queryset.get(pk=artist_id)
        return self.serializer_class(artist_only)

    def _get_artist_does_not_exist_response(self):
        return get_error_response(error_message='Artist with given id does not exist',
                                       response_status=status.HTTP_400_BAD_REQUEST)
