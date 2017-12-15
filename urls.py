from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^graph/[0-1][0-9]$', views.graph, name='graph'),
]