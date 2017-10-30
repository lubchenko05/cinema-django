from django.conf.urls import url
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from api.views import FilmView, CinemaView, CinemaDetailView, PosterView, PosterDetailView, FilmDetailView

urlpatterns = [
    url(r'^token-auth/', obtain_jwt_token),
    url(r'^token-refresh/', refresh_jwt_token),
    url(r'^token-verify/', verify_jwt_token),

    url(r'^film/$', FilmView.as_view(), name='film'),
    url(r'^film/(?P<pk>[0-9]+)/$', FilmDetailView.as_view(), name='film-detail'),

    url(r'poster/$', PosterView.as_view(), name='poster'),
    url(r'^poster/(?P<pk>[0-9]+)/$', PosterDetailView.as_view(), name='poster-detail'),

    url(r'^cinema/$', CinemaView.as_view(), name='cinema'),
    url(r'^cinema/(?P<pk>[0-9]+)/$', CinemaDetailView.as_view(), name='cinema-detail'),

]
