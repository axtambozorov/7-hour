from django.urls import URLPattern, path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('room/<str:pk>/', room, name='room'),

    path('create_room/',createRoom,name='create_room'),
    path('update_room/<str:pk>/',updateRoom,name='update_room'),
    path('delete_room/<str:pk>/',deleteRoom,name='delete_room'),
    path('delete_message/<str:pk>/',deleteMessage,name='delete_message'),

    path('login/',loginPage,name='login'),
    path('logout/',logoutPage,name='logout'),
    path('register/',register,name='register'),

    path('profile/<str:pk>/',userProfile,name='profile'),
    path('edit_profile/',updateProfile,name='edit_profile'),

    
]