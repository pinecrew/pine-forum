from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^thread/(?P<thread_id>\d+)/$', hello.views.thread),
    url(r'^thread/\d+/post/(?P<message_id>\d+)$', hello.views.message),
    url(r'^admin/', include(admin.site.urls)),
]
