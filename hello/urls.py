from django.conf.urls import include, url

from . import views

urlpatterns = [url(r'^requestWork', views.request_work, name='requestWork'),
               url(r'^responseResult', views.response_result, name='responseResult'),
               url(r'^$', views.index, name='index'),
]