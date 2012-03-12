from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.home', name='home'),  
    url(r'^admin/', include(admin.site.urls)),
    url(r'^budget/',include('budget.urls')),
    url(r'^login/?$', 'users.views.twitter_login', name='login'),
    url(r'^logout/?$', 'users.views.twitter_logout', name='lgout'),
    url(r'^login/authenticated/?$', 'users.views.twitter_authenticated', name='authenticated'),
    
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}, name='static'),

)
