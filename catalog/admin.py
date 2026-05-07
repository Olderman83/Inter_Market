from django.contrib import admin
from .models import Category, Product, Contact
from .models import BlogPost


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name',]
    search_fields = ['name',]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category', 'created_at']
    list_display_links = ['name']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['price']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'image', 'category')
        }),
        ('Цены и финансы', {
            'fields': ('price',)
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'phone']
    readonly_fields = ['created_at']


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
