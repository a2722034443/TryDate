from django.urls import path
from . import views

urlpatterns = [
    path('rooms/', views.room_list, name='room-list'),
    path('rooms/<int:room_id>/messages/', views.room_messages, name='room-messages'),
    path('rooms/<int:room_id>/upload/', views.upload_image, name='upload-image'),
    path('report/', views.report_user, name='report-user'),
    path('block/<uuid:user_id>/', views.block_user, name='block-user'),
    path('unblock/<uuid:user_id>/', views.unblock_user, name='unblock-user'),
]
