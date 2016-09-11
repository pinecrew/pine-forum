from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^thread/(?P<thread_id>\d+)/$', hello.views.thread, name='thread'),
    url(r'^thread/(?P<thread_id>\d+)/post/(?P<message_id>\d+)$', hello.views.message, name='message'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/', hello.views.login, name='login',)
]
