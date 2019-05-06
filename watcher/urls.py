from django.urls import path
from . import views


urlpatterns = [
    path('', views.room_list, name='room_list'),
    path('save/',views.seatInfo_save),
    path('room/new/', views.room_new, name='room_new'),
    path('room/detail/<str:address>/', views.room_detail, name='room_detail'),
    path('room/edit/<str:address>/', views.room_edit, name='room_edit'),
    path('room/all/',views.room_all, name='room_all'),
    path('room/test/',views.room_test, name='room_test'),
    # path('room/seat/<str:name>/',views.room_seat),
    path('room/seat/',views.room_seat),
    path('room/seat/<str:pcname>/',views.room_seat),
    path('room/info/<str:pcname>/',views.room_info),
    path('room/<str:region>/',views.room_region),

]