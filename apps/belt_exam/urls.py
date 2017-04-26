from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^quotes$', views.quotes),
    url(r'^postquote$', views.postquote),
    url(r'^favoritequote/(?P<id>\d+)$', views.favoritequote),
    url(r'^user/(?P<id>\d+)$', views.user_page),
    url(r'^removequote/(?P<id>\d+)$', views.removequote),
    url(r'^logout$', views.logout)
]
