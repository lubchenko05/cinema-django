from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from root.models import Cinema, Genre, FilmPoster, Film, FilmSession, CinemaPlace


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


class FilmSessionSerializer(serializers.ModelSerializer):

    class Meta:
        model = FilmSession
        fields = ['id', 'film', 'cinema', 'datetime']


class FilmSessionDetailSerializer(serializers.ModelSerializer):
    free_places = CinemaPlacesSerializer(many=True, read_only=True)

    class Meta:
        model = FilmSession
        fields = ['id', 'film', 'cinema', 'datetime', 'free_places']


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
