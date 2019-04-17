from django.urls import path
from . import views


urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('room/new/', views.room_new, name='room_new'),
    path('room/detail/<str:address>/', views.room_detail, name='room_detail'),
    path('room/edit/<str:address>/', views.room_edit, name='room_edit'),
]