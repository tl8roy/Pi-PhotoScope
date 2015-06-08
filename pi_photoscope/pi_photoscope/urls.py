from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^take/$', views.take, name='take'),
    url(r'^view/$', views.view, name='view'),
    url(r'^download/(?P<photo_id>[0-9]+)/$', views.download, name='download'),
    url(r'^delete/(?P<photo_id>[0-9]+)/$', views.delete, name='delete'),
]