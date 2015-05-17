from django.views.generic.base import RedirectView
from django.conf.urls import patterns, include, url
from django.contrib import admin
from . import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'bus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),

    url(r'^$', 'busapp.views.index_view', name='index_view'),
    url(r'^display$', 'busapp.views.display_view', name='display_view'),
    url(r'^buses$', 'busapp.views.buses_view', name='buses_view'),
    url(r'^map$', 'busapp.views.map_view', name='map_view'),
    url(r'^login$', 'busapp.views.login_view', name='login_view'),
    url(r'^accounts/login/$', 'busapp.views.login_view', name='login_view'),
    url(r'^logout$', 'busapp.views.logout_view', name='logout_view'),
    url(r'^setup$', 'busapp.views.setup_view', name='setup_view')
)
