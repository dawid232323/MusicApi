from .song_serializer import ReducedSongSerializer
from rest_framework import serializers

from musicApiApp.models import Album, Song


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'


class AlbumSongsSerializer(AlbumSerializer):
    songs = ReducedSongSerializer(many=True)

    def create(self, validated_data):
        songs = validated_data.pop('songs')
        Song.objects.update()
        new_album = Album.objects.create(**validated_data)
        for single_song in songs:
            Song.objects.create(album=new_album, **single_song)
        return new_album
