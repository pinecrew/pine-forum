from django.urls import path
from django.contrib import admin
from rest_framework import routers

from forum import views


router = routers.SimpleRouter()
router.register(r'messages', views.MessageViewSet)

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('thread/<int:pk>/', views.ThreadDetailView.as_view(), name='thread'),
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('newthread/', views.ThreadCreateView.as_view(), name='newthread'),
    path('thread/<int:thread_id>/newmessage/', views.MessageCreateView.as_view(), name='newmessage'),
    path('user/<str:username>/', views.ProfileView.as_view(), name='profile'),
    path('newuser/', views.user_new, name='newuser'),
    path('changepassword/', views.change_password, name='change_password'),
    *router.urls
]
