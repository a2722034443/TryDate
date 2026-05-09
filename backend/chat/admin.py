from django.contrib import admin
from .models import ChatRoom, Message, Report


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'match', 'is_active', 'last_message_at']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'msg_type', 'content', 'created_at']
    list_filter = ['msg_type']

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['reporter', 'target_user', 'reason', 'status', 'created_at']
    list_filter = ['status', 'reason']
