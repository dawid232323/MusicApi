from rest_framework import serializers

from musicApiApp.models import Artist
from .album_serializer import ReducedAlbumSerializer


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'


class DisplayAlbumsArtistSerializer(ArtistSerializer):
    albums = ReducedAlbumSerializer(many=True)
