from django.contrib import admin
from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'icon', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


class ProductImageInline(admin.TabularInline):
    """
    Show product images inline within the Product admin page.
    """
    model = ProductImage
    extra = 1
    readonly_fields = ['uploaded_at']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'seller', 'category', 'price',
        'condition', 'is_sold', 'is_active', 'created_at'
    ]
    list_filter = ['is_sold', 'is_active', 'condition', 'category']
    search_fields = ['title', 'description', 'seller__email']
    list_editable = ['is_sold', 'is_active']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ProductImageInline]

    fieldsets = (
        ('Listing Info', {
            'fields': ('title', 'description', 'price', 'condition', 'category', 'location')
        }),
        ('Ownership', {
            'fields': ('seller',)
        }),
        ('Status', {
            'fields': ('is_sold', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'uploaded_at']
    list_filter = ['uploaded_at']