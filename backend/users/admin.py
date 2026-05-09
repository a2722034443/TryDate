from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, BlackList, VerificationCode


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['nickname', 'email', 'phone', 'gender', 'status', 'questionnaire_completion', 'created_at']
    list_filter = ['gender', 'status', 'grade', 'college_direction']
    search_fields = ['nickname', 'email', 'phone']
    ordering = ['-created_at']
    fieldsets = (
        (None, {'fields': ('email', 'phone', 'password')}),
        ('基本信息', {'fields': ('nickname', 'gender', 'gender_preference', 'birth_year', 'grade', 'college_direction', 'avatar', 'bio')}),
        ('状态', {'fields': ('status', 'questionnaire_completion', 'is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email', 'nickname', 'gender', 'password1', 'password2')}),
    )


@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = ['blocker', 'blocked', 'created_at']


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = ['target', 'code_type', 'code', 'is_used', 'created_at']
    list_filter = ['code_type', 'is_used']
