from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import forum.views

# Examples:
# url(r'^$', 'pinecrew.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', forum.views.index, name='index'),
    url(r'^thread/(?P<thread_id>\d+)/$', forum.views.thread, name='thread'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', forum.views.login, name='login'),
    url(r'^logout/$', forum.views.logout, name='logout'),
    url(r'^newthread/$', forum.views.thread_new, name='newthread'),
    url(r'^thread/(?P<thread_id>\d+)/newmessage/$', forum.views.message_new, name='newmessage'),
    url(r'^message/(?P<message_id>\d+)_t/$', forum.views.message_tog, name='messagetog'),
    url(r'^message/(?P<message_id>\d+)/$', forum.views.message, name='message'),
]
