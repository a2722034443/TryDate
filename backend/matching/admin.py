from django.contrib import admin
from .models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['week_number', 'user_a', 'user_b', 'compatibility_score', 'status', 'matched_at']
    list_filter = ['status', 'week_number']
    search_fields = ['user_a__nickname', 'user_b__nickname']
