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
    url(r'^thread/(?P<thread_id>\d+)/post/(?P<message_id>\d+)$', forum.views.message, name='message'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', forum.views.login, name='login'),
    url(r'^logout/$', forum.views.logout, name='logout'),
    url(r'^thread/(?P<thread_id>\d+)/newmessage/$', forum.views.new_message, name='newmessage'),
    url(r'^newthread/$', forum.views.new_thread, name='newthread'),
]