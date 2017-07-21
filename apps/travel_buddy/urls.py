from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^main$', views.index, name='index'),
    url(r'^register$', views.register, name='register'),
    url(r'^authenticate$', views.authenticate, name='login'),
    url(r'^travels$', views.home, name='home'),
    url(r'^travels/destination/(?P<trip_id>\d+)$', views.read_destination, name='destination'),
    url(r'^travels/add$', views.add, name='add'),
    url(r'^travels/create$', views.create, name='create'),
    url(r'^travels/join/(?P<trip_id>\d+)$', views.join, name='join'),
    url(r'^logout$', views.logout, name='logout')
]
