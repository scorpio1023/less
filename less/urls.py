from django.conf.urls import patterns, include, url
import settings
from app.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'less.views.home', name='home'),
    # url(r'^less/', include('less.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^static/(?P<path>.*)','django.views.static.serve',{'document_root': settings.STATIC_URL}),
    url(r'^app/$',myapp),
    url(r'^app/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/$',detail),
    url(r'^app/gh/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})/$',gethostinfo),
)
