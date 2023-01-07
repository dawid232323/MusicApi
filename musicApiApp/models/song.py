from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


from musicApiApp.models import Album


class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='songs')
    name = models.CharField(max_length=100)
    duration = models.FloatField(default=1)
    rating = models.FloatField(default=3, validators=[
        MaxValueValidator(5), MinValueValidator(1)
    ])
    album_position = models.IntegerField(validators=[MinValueValidator(1)])
