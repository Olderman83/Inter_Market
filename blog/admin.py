from django.contrib import admin
from .models import BlogPost


# Register your models here.
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'is_published', 'views_count']
    list_display_links = ['title']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'content']
    list_editable = ['is_published']
    readonly_fields = ['views_count', 'created_at']
    list_per_page = 20

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content', 'preview')
        }),
        ('Публикация', {
            'fields': ('is_published',)
        }),
        ('Статистика', {
            'fields': ('views_count', 'created_at'),
            'classes': ('collapse',)
        }),
    )
