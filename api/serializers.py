from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from root.models import Cinema, Genre, FilmPoster, Film, FilmSession, CinemaPlace, FilmSessionPlace


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class GenreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class FilmPosterSerializer(serializers.ModelSerializer):

    class Meta:
        model = FilmPoster
        fields = ['id', 'image', 'film']


class CinemaPlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaPlace
        fields = ['id', 'row', 'position']


class FilmSessionPlaceSerializer(serializers.ModelSerializer):
    place = CinemaPlacesSerializer(read_only=True)

    class Meta:
        model = FilmSessionPlace
        fields = ['id', 'place', 'film_session', 'price', 'is_free']


class FilmSessionSerializer(serializers.ModelSerializer):
    start_price = serializers.FloatField(write_only=True)

    class Meta:
        model = FilmSession
        fields = ['id', 'film', 'cinema', 'datetime', 'start_price']

    def create(self, validated_data):
        film = validated_data['film']
        cinema = validated_data['cinema']
        datetime = validated_data['datetime']
        start_price = validated_data['start_price'] if 'start_price' in validated_data else 0.0
        film = Film.objects.filter(pk=film).first()
        cinema = Cinema.objects.filter(pk=cinema).first()

        if not film:
            raise ValidationError('Film was not found!')
        if not cinema:
            raise ValidationError('cinema was not found!')

        for session in cinema.film_sessions.all():
            if session.datetime < datetime < session.datetime + session.film.time:
                raise ValidationError('This time is occupied by another event!')

        film_session = FilmSession.objects.create(film=film, cinema=cinema, datetime=datetime)
        film_session.save()

        for cinema_place in cinema.places.all():
            session = FilmSessionPlace.objects.create(place=cinema_place,
                                                      film_session=film_session,
                                                      price=start_price+cinema_place.row*5)
            session.save()

        return film_session


class FilmSessionDetailSerializer(serializers.ModelSerializer):
    places = FilmSessionPlaceSerializer(many=True, read_only=True)

    class Meta:
        model = FilmSession
        fields = ['id', 'film', 'cinema', 'datetime', 'places']


class FilmCreateSerializer(serializers.ModelSerializer):
    posters = FilmPosterSerializer(many=True)

    class Meta:
        model = Film
        fields = ['id', 'name', 'description', 'start_date', 'time', 'genre']


class FilmSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    posters = FilmPosterSerializer()

    class Meta:
        model = Film
        fields = ['id', 'name', 'description', 'start_date', 'time', 'genre', 'posters']


class CinemaSerializer(serializers.ModelSerializer):
    places = serializers.ListField(write_only=True)

    class Meta:
        model = Cinema
        fields = ['id', 'name', 'places']

    def create(self, validated_data):
        cinema = Cinema.objects.create(name=validated_data['name'])
        places = validated_data['places'] if 'places' in validated_data else None
        if places:
            for row, column in enumerate(validated_data['places']):
                try:
                    column = int(column)
                except:
                    continue
                if column > 0:
                    for place in range(1, column+1):
                        CinemaPlace.objects.create(row=row+1, position=place, cinema=cinema)

        return cinema


class CinemaDetailSerializer(serializers.ModelSerializer):
    places = CinemaPlacesSerializer(many=True,  read_only=True)

    class Meta:
        model = Cinema
        fields = ['id', 'name', 'places']


class FilmDetailSerializer(serializers.ModelSerializer):
    events = FilmSessionSerializer(many=True, read_only=True)

    class Meta:
        model = Film
        fields = ['id', 'name', 'description', 'start_date', 'time', 'genre', 'events']


class UserSerializer(serializers.ModelSerializer):
    places = CinemaPlacesSerializer(read_only=True, many=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password', 'places']
