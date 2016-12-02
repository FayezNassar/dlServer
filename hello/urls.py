from django.conf.urls import include, url

from . import views

urlpatterns = [url(r'^get_file_url', views.get_file_url, name='get_file_url'),
               url(r'^$', views.index, name='index'),
]