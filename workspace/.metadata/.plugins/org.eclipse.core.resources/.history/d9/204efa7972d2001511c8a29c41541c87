from django.conf.urls import patterns, url
from rango import views

# URL mapping 
urlpatterns = patterns('',
                       # Any empty string after /rango/ will invoke views.index
                       url(r'^$', views.index, name="index"),
                       url(r'^about/', views.about, name="about"),
)