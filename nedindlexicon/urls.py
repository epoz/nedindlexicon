from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'nedindlexicon.views.home', name='home'),
    url(r'^search/$', 'nedindlexicon.views.search', name='search'),
    url(r'^trefwoord/([0-9]+)$', 'nedindlexicon.views.trefwoordview', name='trefwoord'),
    url(r'^naslag/$', 'nedindlexicon.views.naslagview', name='naslag'),

    url(r'^admin/', include(admin.site.urls)),
)
