from django.conf.urls import url
from . import views

# ULS fro app cursoOnline
app_name = 'cursoOnline'
urlpatterns = [
    # ex: /cursoOnline/
    url(r'^$', views.index, name='index'),
    # ex: /cursoOnline/5/logInSignIn/
    url(r'^(?P<curso_id>[0-9]+)/logInSignIn/$', views.logInSignIn, name='logInSignIn'),
    # ex: /cursoOnline/5/logInSignIn/form/
    url(r'^(?P<curso_id>[0-9]+)/logInSignIn/form/$', views.form, name='form'),
    # ex: /cursoOnline/3/1/cursoHub/
    url(r'^(?P<curso_id>[0-9]+)/(?P<participante_id>[0-9]+)/cursoHub/$', views.cursoHub, name='cursoHub'),
    # ex: /cursoOnline/3/1/cursoVideos/
    url(r'^(?P<curso_id>[0-9]+)/(?P<participante_id>[0-9]+)/cursoVideos/$', views.cursoVideos, name='cursoVideos'),
    # ex: /cursoOnline/3/1/cursoQuestoes/
    url(r'^(?P<curso_id>[0-9]+)/(?P<participante_id>[0-9]+)/cursoQuestoes/$', views.cursoQuestoes, name='cursoQuestoes'),
    # ex: /cursoOnline/3/1/cursoChat/
    url(r'^(?P<curso_id>[0-9]+)/(?P<participante_id>[0-9]+)/cursoChat/$', views.cursoChat, name='cursoChat'),
    # ex: /cursoOnline/3/1/cursoQuestoes/right/
    url(r'^(?P<curso_id>[0-9]+)/(?P<participante_id>[0-9]+)/cursoQuestoes/right/$', views.right, name='right'),
    # ex: /cursoOnline/3/1/cursoQuestoes/wrong/
    url(r'^(?P<curso_id>[0-9]+)/(?P<participante_id>[0-9]+)/cursoQuestoes/wrong/$', views.wrong, name='wrong'),
    # ex: /cursoOnline/3/1/cursoFim/
    url(r'^(?P<curso_id>[0-9]+)/(?P<participante_id>[0-9]+)/cursoFim/$', views.cursoFim, name='cursoFim'),
]