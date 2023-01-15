from django.db import models

from .artist import Artist
from .genre import Genre


class Album(models.Model):
    name = models.CharField(max_length=100)
    year = models.DateField()
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, related_name='albums', default=1)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='albums')
