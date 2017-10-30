from django.shortcuts import render
from rest_framework import status

from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsStaffOrReadOnly
from api.serializers import FilmSerializer, FilmSessionSerializer, CinemaSerializer, FilmCreateSerializer, \
    FilmDetailSerializer, FilmPosterSerializer, CinemaDetailSerializer
from root.models import Film, FilmSession, Cinema, FilmPoster


class FilmView(ListCreateAPIView):
    model = Film
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = FilmCreateSerializer
    queryset = Film.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = FilmSerializer(self.queryset, many=True)
        return Response(serializer.data)


class FilmDetailView(RetrieveDestroyAPIView):
    permission_classes = [IsStaffOrReadOnly]

    def get(self, request, pk):
        queryset = FilmPoster.objects.filter(pk=pk).first()
        if queryset:
            return Response(FilmDetailSerializer(queryset).data)
        else:
            return Response(data={'error': 'Not Found (404)'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        queryset = FilmPoster.objects.filter(pk=pk).first()
        if queryset:
            queryset.delete()
            return Response(data={'ok': 'Deleted'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'error': 'Not Found (404)'}, status=status.HTTP_404_NOT_FOUND)


class PosterView(ListCreateAPIView):
    model = Cinema
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = FilmPosterSerializer
    queryset = FilmPoster.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = FilmPosterSerializer(self.queryset, many=True)
        return Response(serializer.data)


class PosterDetailView(RetrieveDestroyAPIView):
    permission_classes = [IsStaffOrReadOnly]

    def get(self, request, pk):
        queryset = FilmPoster.objects.filter(pk=pk).first()
        if queryset:
            return Response(FilmPosterSerializer(queryset).data)
        else:
            return Response(data={'error': 'Not Found (404)'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        queryset = FilmPoster.objects.filter(pk=pk).first()
        if queryset:
            queryset.delete()
            return Response(data={'ok': 'Deleted'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'error': 'Not Found (404)'}, status=status.HTTP_404_NOT_FOUND)


class CinemaView(ListCreateAPIView):
    model = Cinema
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = CinemaSerializer
    queryset = Cinema.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = CinemaSerializer(self.queryset, many=True)
        return Response(serializer.data)


class CinemaDetailView(RetrieveDestroyAPIView):
    permission_classes = [IsStaffOrReadOnly]

    def get(self, request, pk):
        queryset = Cinema.objects.filter(pk=pk).first()
        if queryset:
            return Response(CinemaDetailSerializer(queryset).data)

    def delete(self, request, pk):
        queryset = Cinema.objects.filter(pk=pk).first()
        if queryset:
            queryset.delete()
            return Response(data={'ok': 'Deleted'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'error': 'Not Found (404)'}, status=status.HTTP_404_NOT_FOUND)


class FilmSessionView(ListCreateAPIView):
    model = FilmSession
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = FilmSessionSerializer
    queryset = FilmSession.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = FilmSessionSerializer(self.queryset, many=True)
        return Response(serializer.data)


class FilmSessionDetailView(RetrieveDestroyAPIView):
    permission_classes = [IsStaffOrReadOnly]

    def get(self, request, pk):
        queryset = FilmSession.objects.filter(pk=pk).first()
        if queryset:
            return Response(FilmSessionSerializer(queryset).data)

    def delete(self, request, pk):
        queryset = FilmSession.objects.filter(pk=pk).first()
        if queryset:
            queryset.delete()
            return Response(data={'ok': 'Deleted'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'error': 'Not Found (404)'}, status=status.HTTP_404_NOT_FOUND)




