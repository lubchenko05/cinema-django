import datetime

from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.compat import MaxValueValidator, MinValueValidator


UserModel = get_user_model()


class Film(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField(default=datetime.datetime.now().date(), blank=False)
    time = models.TimeField(blank=False)
    genre = models.ForeignKey(Genre, related_name='genres')

    def __str__(self):
        return self.name


class FilmSession(models.Model):
    film = models.ForeignKey(Film, related_name='events')
    price = models.FloatField(default=0.0)
    datetime = models.DateTimeField(blank=False)

    def __str__(self):
        return '%s - %s' % (self.film.name, self.datetime)


class Cinema(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_free_places(self):
        return self.places.filter(owner=None)


class CinemaPlaces(models.Model):
    cinema = models.ForeignKey(Cinema, related_name='places')
    row = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])
    position = models.ImageField(validators=[MaxValueValidator(100), MinValueValidator(1)])
    owner = models.ForeignKey(UserModel, related_name='places', null=True)

    def __str__(self):
        return self.cinema.name


class FilmPoster(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='posters')
    image = models.ImageField(upload_to='Posters', blank=False)

    def __str__(self):
        return self.film.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
