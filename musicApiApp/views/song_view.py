from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from musicApiApp.models import Song
from musicApiApp.serializers import ReducedSongSerializer
from musicApiApp.utils.error_utils import get_error_response


class SongView(ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = ReducedSongSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        return Response(self.serializer_class(self.queryset, many=True).data, status=status.HTTP_200_OK)

    def retrieve(self, request, song_id=None, *args, **kwargs):
        retrieved_song: Song
        try:
            retrieved_song = self.queryset.get(pk=song_id)
        except ObjectDoesNotExist:
            return self._song_dose_not_exist_response()
        serialized_song = self.serializer_class(retrieved_song)
        return Response(serialized_song.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        request_body = request.data
        serialized_body = self.serializer_class(data=request_body)
        serialized_body.is_valid(raise_exception=True)
        serialized_body.save()
        return Response(serialized_body.data, status=status.HTTP_201_CREATED)

    def update(self, request, song_id=None, *args, **kwargs):
        song_to_update: Song
        try:
            song_to_update = self.queryset.get(pk=song_id)
        except ObjectDoesNotExist:
            return self._song_dose_not_exist_response()
        song_body = request.data
        serialised_song = self.serializer_class(instance=song_to_update, data=song_body, partial=True)
        serialised_song.is_valid(raise_exception=True)
        serialised_song.save()
        return Response(serialised_song.data, status=status.HTTP_200_OK)

    def destroy(self, request, song_id=None, *args, **kwargs):
        song_to_delete: Song
        try:
            song_to_delete = self.queryset.get(pk=song_id)
        except ObjectDoesNotExist:
            return self._song_dose_not_exist_response()
        song_to_delete.delete()
        return Response(status=status.HTTP_200_OK)

    def _song_dose_not_exist_response(self) -> JsonResponse:
        return get_error_response(error_message='Song with given id does not exist',
                                  response_status=status.HTTP_400_BAD_REQUEST)