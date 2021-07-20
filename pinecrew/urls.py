from django.urls import path

from django.contrib import admin

from forum import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('thread/<int:pk>/', views.ThreadDetailView.as_view(), name='thread'),
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('newthread/', views.ThreadCreateView.as_view(), name='newthread'),
    path('thread/<int:thread_id>/newmessage/', views.MessageCreateView.as_view(), name='newmessage'),
    path('message/<int:message_id>_t/', views.message_tog, name='messagetog'),
    path('message/<int:message_id>/', views.message, name='message'),
    path('user/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('newuser/', views.user_new, name='newuser'),
    path('changepassword/', views.change_password, name='change_password'),
]
