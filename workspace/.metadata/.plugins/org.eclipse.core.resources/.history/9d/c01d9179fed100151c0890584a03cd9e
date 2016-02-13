from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       # Matches string rango/ and passes the remainder to rango.urls for match
                       url(r'^rango/', include('rango.urls')),
)
