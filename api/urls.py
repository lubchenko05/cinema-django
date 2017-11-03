from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from api.views import FilmView, CinemaView, CinemaDetailView, PosterView, PosterDetailView, FilmDetailView, \
    FilmSessionView, FilmSessionDetailView, GenreDetailView, find_films, ticket_buy, UserCreateView, UserDetailView, \
    GenreView

urlpatterns = [
    url(r'^token-auth/', obtain_jwt_token),
    url(r'^token-refresh/', refresh_jwt_token),
    url(r'^token-verify/', verify_jwt_token),

    url(r'^film/$', FilmView.as_view(), name='film'),
    url(r'^film/(?P<pk>[0-9]+)/$', FilmDetailView.as_view(), name='film-detail'),
    url(r'^film/search/$', find_films, name='film-find'),

    url(r'poster/$', PosterView.as_view(), name='poster'),
    url(r'^poster/(?P<pk>[0-9]+)/$', PosterDetailView.as_view(), name='poster-detail'),

    url(r'^cinema/$', CinemaView.as_view(), name='cinema'),
    url(r'^cinema/(?P<pk>[0-9]+)/$', CinemaDetailView.as_view(), name='cinema-detail'),

    url(r'^event/$', FilmSessionView.as_view(), name='event'),
    url(r'^event/(?P<pk>[0-9]+)/$', FilmSessionDetailView.as_view(), name='cinema-detail'),

    url(r'buy/(?P<pk>[0-9]+)/$', ticket_buy, name='buy-ticket'),

    url(r'^genre/$', GenreView.as_view(), name='genre'),
    url(r'^genre/(?P<pk>[0-9]+)/$', GenreDetailView.as_view(), name='genre-detail'),

    url(r'^registration/$', UserCreateView.as_view(), name='user-create'),
    url(r'^user/$', UserDetailView.as_view(), name='user-detail'),

    url(r'^docs/', include('rest_framework_docs.urls')),

]
