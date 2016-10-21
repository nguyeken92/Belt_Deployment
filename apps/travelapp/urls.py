from django.conf.urls import url
from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  url(r'^login$', views.login, name='login'),
  url(r'^register$', views.register, name='register'),
  url(r'^home$', views.home, name='home'),
  url(r'^logoff$', views.logoff, name='logoff'),
  url(r'^add$', views.add, name='add'),
  url(r'^create$', views.create, name='create'),
  url(r'^travel/destination/(?P<travel_id>\d+)$', views.show, name='show'),
  url(r'^join/(?P<id>\d+)$', views.join, name='join'),
]
