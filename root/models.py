import datetime

from django.db import models


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


class FilmPoster(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='posters')
    image = models.ImageField(upload_to='Posters', blank=False)

    def __str__(self):
        return self.film.name


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
