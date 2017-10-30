from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes

from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsStaffOrReadOnly
from api.serializers import FilmSerializer, FilmSessionSerializer, CinemaSerializer, FilmCreateSerializer, \
    FilmDetailSerializer, FilmPosterSerializer, CinemaDetailSerializer, FilmSessionDetailSerializer, \
    GenreDetailSerializer, FilmSessionPlaceSerializer, UserSerializer
from root.models import Film, FilmSession, Cinema, FilmPoster, Genre, FilmSessionPlace


class UserCreateView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    queryset = get_user_model().objects.all()
    permission_classes = [IsAuthenticated, ]

    def get(self, request, format=None):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)


class FilmView(ListCreateAPIView):
    model = Film
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = FilmCreateSerializer
    queryset = Film.objects.all()

    def list(self, request, *args, **kwargs):
        serializer = FilmSerializer(self.queryset.all(), many=True)
        return Response(serializer.data)


class FilmDetailView(RetrieveDestroyAPIView):
    permission_classes = [IsStaffOrReadOnly]

    def get(self, request, pk):
        queryset = Film.objects.filter(pk=pk).first()
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
        serializer = FilmPosterSerializer(self.queryset.all(), many=True)
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
        serializer = CinemaSerializer(self.queryset.all(), many=True)
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
        serializer = FilmSessionSerializer(self.queryset.all(), many=True)
        return Response(serializer.data)


class FilmSessionDetailView(RetrieveDestroyAPIView):
    permission_classes = [IsStaffOrReadOnly]

    def get(self, request, pk):
        queryset = FilmSession.objects.filter(pk=pk).first()
        if queryset:
            return Response(FilmSessionDetailSerializer(queryset).data)

    def delete(self, request, pk):
        queryset = FilmSession.objects.filter(pk=pk).first()
        if queryset:
            queryset.delete()
            return Response(data={'ok': 'Deleted'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'error': 'Not Found (404)'}, status=status.HTTP_404_NOT_FOUND)


class GenreDetailView(RetrieveAPIView):
    queryset = Genre.objects.all()
    permission_classes = ([AllowAny, ])
    serializer_class = GenreDetailSerializer


@api_view(['POST'])
@permission_classes([AllowAny, ])
def find_films(request):
    name = request.data['name'] if 'name' in request.data else None
    if not name:
        return Response(data={"validation_error": "name is required"}, status=status.HTTP_400_BAD_REQUEST)
    queryset = []
    for film in Film.objects.all():
        if name.lower() in film.name.lower():
            queryset.append(film)
    if not queryset:
        return Response({"error": 'Not Found (404)'}, status=status.HTTP_404_NOT_FOUND)
    return Response(data=FilmSerializer(queryset, many=True).data)


@api_view(['GET'])
@permission_classes([IsAuthenticated, ])
def ticket_buy(request, pk):
    ticket = FilmSessionPlace.objects.filter(pk=pk).first()
    if not ticket:
        return Response({"error": 'Not Found (404)'}, status=status.HTTP_404_NOT_FOUND)
    if ticket.is_free():
        ticket.owner = request.user
        ticket.save()
        return Response(data={"ok": "Purchase successful completed", "ticket": FilmSessionPlaceSerializer(ticket).data})
    else:
        if request.user == ticket.owner:
            return Response(data={"error": "You already have this ticket"}, status=status.HTTP_403_FORBIDDEN)
        else:
            return Response(data={"error": "This ticket is occupied by another user!"}, status=status.HTTP_403_FORBIDDEN)

