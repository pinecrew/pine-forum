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
    url(r'^thread/(?P<thread_id>\d+)/newmessage/$', forum.views.new_message, name='newmessage'),
    url(r'^newthread/$', forum.views.new_thread, name='newthread'),
    url(r'^thread/\d+/edit/$', forum.views.edit_message, name='editmessage'),
    url(r'^thread/\d+/delete/$', forum.views.del_message, name='delmessage'),
    url(r'^thread/\d+/restore/$', forum.views.res_message, name='resmessage'),
]
