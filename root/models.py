import datetime

from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.compat import MaxValueValidator, MinValueValidator


UserModel = get_user_model()


class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Film(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField(default=datetime.datetime.now().date(), blank=False)
    time = models.TimeField(blank=False)
    genre = models.ManyToManyField(Genre, related_name='films')

    def __str__(self):
        return self.name


class Cinema(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class FilmSession(models.Model):
    film = models.ForeignKey(Film, related_name='events')
    cinema = models.ForeignKey(Cinema, related_name='film_sessions', null=False)
    datetime = models.DateTimeField(blank=False)

    def __str__(self):
        return '%s - %s' % (self.film.name, self.datetime)

    def free_places(self):
        return self.places.filter(owner=None).all()


class CinemaPlace(models.Model):
    cinema = models.ForeignKey(Cinema, related_name='places', blank=False, null=True, on_delete=models.CASCADE)
    row = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])
    position = models.IntegerField(validators=[MaxValueValidator(100), MinValueValidator(1)])

    class Meta:
        unique_together = ("cinema", "row", "position")

    def __str__(self):
        return "%s - %s" % (self.row, self.position)


class FilmSessionPlace(models.Model):
    place = models.ForeignKey(CinemaPlace)
    film_session = models.ForeignKey(FilmSession, related_name='places')
    price = models.FloatField(validators=[MinValueValidator(0)])
    owner = models.ForeignKey(UserModel, blank=True, related_name='tickets')


class FilmPoster(models.Model):
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='posters')
    image = models.ImageField(upload_to='Posters', blank=False)

    def __str__(self):
        return self.film.name
