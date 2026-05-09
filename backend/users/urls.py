from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('send-code/', views.send_code, name='send-code'),
    path('register/', views.register, name='register'),
    path('login/', views.login_with_code, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
