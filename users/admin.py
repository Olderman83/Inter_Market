from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Настройка админки для кастомной модели пользователя"""
    list_display = ['email', 'first_name', 'last_name', 'phone', 'country', 'is_active', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'country', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name', 'phone']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'avatar', 'phone', 'country')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    ordering = ['email']
    list_per_page = 20
