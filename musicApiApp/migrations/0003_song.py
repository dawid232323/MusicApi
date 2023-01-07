# Generated by Django 4.1.5 on 2023-01-07 10:42

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musicApiApp', '0002_genre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('duration', models.FloatField(default=1)),
                ('rating', models.FloatField(default=3, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('album_position', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicApiApp.album')),
            ],
        ),
    ]