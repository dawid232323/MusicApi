from rest_framework import serializers

from musicApiApp.models import Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


class ReducedSongSerializer(SongSerializer):
    class Meta:
        model = Song
        exclude = ('album', )
