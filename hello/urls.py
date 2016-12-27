from django.conf.urls import include, url

from . import views

urlpatterns = [url(r'^deepLearning', views.deep_learning, name='deepLearning'),
               url(r'^joinSystem', views.join_system, name='joinSystem'),
               url(r'^$', views.index, name='index'),
]