from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

from cinema_django import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)