from django.db import models


class Album(models.Model):
    name = models.CharField(max_length=100)
    year = models.DateField()
