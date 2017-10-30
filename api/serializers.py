import time
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import timedelta
from root.models import Cinema, Genre, FilmPoster, Film, FilmSession, CinemaPlace, FilmSessionPlace


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['id', 'name']


class FilmPosterSerializer(serializers.ModelSerializer):

    class Meta:
        model = FilmPoster
        fields = ['id', 'image']


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

        if not film:
            raise ValidationError({"validation_error": 'Film was not found!'})
        if not cinema:
            raise ValidationError({"validation_error": 'Сinema was not found!'})

        t_timestamp_from = time.mktime(datetime.timetuple())
        t_timestamp_to = time.mktime((datetime+timedelta(hours=film.time.hour,
                                                         minutes=film.time.minute,
                                                         seconds=film.time.second
                                                         )).timetuple())
        for session in cinema.film_sessions.all():
            t_from = time.mktime(session.datetime.timetuple())
            t_to = time.mktime((session.datetime+timedelta(hours=session.film.time.hour,
                                                           minutes=session.film.time.minute,
                                                           seconds=session.film.time.second
                                                           )).timetuple())
            if t_from <= t_timestamp_from <= t_to and t_from <= t_timestamp_to <= t_to:
                raise ValidationError({'validation_error': 'This time is occupied by another event!'})

        film_session = FilmSession.objects.create(film=film, cinema=cinema, datetime=datetime)
        film_session.save()

        for cinema_place in cinema.places.all():
            session = FilmSessionPlace.objects.create(place=cinema_place,
                                                      film_session=film_session,
                                                      price=start_price+(cinema_place.row-1)*5)
            session.save()

        return film_session


class FilmSessionDetailSerializer(serializers.ModelSerializer):
    places = FilmSessionPlaceSerializer(many=True, read_only=True)

    class Meta:
        model = FilmSession
        fields = ['id', 'film', 'cinema', 'datetime', 'places']


class FilmCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Film
        fields = ['id', 'name', 'description', 'start_date', 'time', 'genre']


class FilmSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    posters = FilmPosterSerializer(many=True, read_only=True)

    class Meta:
        model = Film
        fields = ['id', 'name', 'description', 'start_date', 'time', 'genre', 'posters']


class GenreDetailSerializer(serializers.ModelSerializer):
    films = FilmSerializer(many=True, read_only=True)

    class Meta:
        model = Genre
        fields = ['id', 'name', 'films']


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
    tickets = FilmSessionPlaceSerializer(read_only=True, many=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email', 'password', 'tickets']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        user = get_user_model().objects.create(username=username)
        user.set_password(password)
        user.save()
        return user
