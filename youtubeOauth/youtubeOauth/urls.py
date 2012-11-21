from django.conf.urls import patterns, include, url
#import os.path
import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from youtubeOauth import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'youtubeOauth.views.home', name='home'),
    # url(r'^youtubeOauth/', include('youtubeOauth.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^register', views.register, name='register'),
    url(r'^login', views.login, name='login'),
    url(r'^home', views.home, name='home'),
    url(r'^data', views.data, name='data'),
    url( r'^static/(?P<path>.*)$', 'django.views.static.serve',{ 'document_root': settings.STATIC_ROOT }),


)
