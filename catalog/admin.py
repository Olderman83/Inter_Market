from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Contact


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['name']
    search_fields = ['name']
    list_per_page = 20


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category', 'owner_display', 'publication_status', 'created_at']
    list_display_links = ['name']
    list_filter = ['category', 'publication_status', 'created_at']
    search_fields = ['name', 'description', 'owner__email']
    list_editable = ['price', 'publication_status']
    list_per_page = 20
    readonly_fields = ['created_at', 'updated_at']

    def owner_display(self, obj):
        if obj.owner:
            return obj.owner.email
        return '-'

    owner_display.short_description = 'Владелец'

    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'image', 'category', 'price')
        }),
        ('Владелец и статус', {
            'fields': ('owner', 'publication_status')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'phone', 'message']
    readonly_fields = ['created_at']
