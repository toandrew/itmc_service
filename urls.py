from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tvserver.views.home', name='home'),
    # url(r'^tvserver/', include('tvserver.foo.urls')),
    url(r'^login$', 'tvserver.server.views.login', name='login'),

    url(r'^getbannermedia$', 'tvserver.server.views.getbannermedia', name='getbannermedia'),
    url(r'^getchannelrecommendmedia$', 'tvserver.server.views.getchannelrecommendmedia', name='getchannelrecommendmedia'),
    url(r'^getchannellist$', 'tvserver.server.views.getchannellist', name='getchannellist'),
    url(r'^getmedialist$', 'tvserver.server.views.getmedialist', name='getmedialist'),
    url(r'^getmediadetail$', 'tvserver.server.views.getmediadetail', name='getmediadetail'),
    url(r'^getmediaurl$', 'tvserver.server.views.getmediaurl', name='getmediaurl'),

    url(r'^setplayhistory$', 'tvserver.server.views.setplayhistory', name='setplayhistory'),
    url(r'^getplayhistory$', 'tvserver.server.views.getplayhistory', name='getplayhistory'),
    url(r'^deleteplayhistory$', 'tvserver.server.views.deleteplayhistory', name='deleteplayhistory'),

    url(r'^setbookmark$', 'tvserver.server.views.setbookmark', name='setbookmark'),
    url(r'^getbookmark$', 'tvserver.server.views.getbookmark', name='getbookmark'),
    url(r'^deletebookmark$', 'tvserver.server.views.deletebookmark', name='deletebookmark'),

    url(r'^searchmedia$', 'tvserver.server.views.searchmedia', name='searchmedia'),

    url(r'^m3u8/(\d+)/(\d+)/(\d+)/m3u8.m3u8$', 'tvserver.server.views.getm3u8', name='get_m3u8'),

    url(r'^cms$', 'tvserver.server.cms.index', name='cms_index'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login',  {'template_name': 'admin/login.html'}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
