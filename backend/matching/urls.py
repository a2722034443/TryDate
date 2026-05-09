from django.urls import path
from . import views

urlpatterns = [
    path('current/', views.current_match, name='current-match'),
    path('<int:match_id>/respond/', views.respond_match, name='respond-match'),
    path('history/', views.match_history, name='match-history'),
    path('trigger/', views.trigger_match, name='trigger-match'),
]
