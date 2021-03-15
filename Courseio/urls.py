from django.contrib import admin
from django.conf.urls import include, url

# Django URLs including admin and all the ones in cursoOnline
urlpatterns = [
    url(r'^cursoOnline/', include('cursoOnline.urls')),
    url(r'^admin/', admin.site.urls),
]
