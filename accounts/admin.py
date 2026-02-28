from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin panel for the User model.
    """
    list_display = ['email', 'username', 'first_name', 'last_name', 'college_name', 'is_active']
    list_filter = ['is_active', 'is_staff', 'college_name']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']

    # Add custom fields to the admin detail view
    fieldsets = UserAdmin.fieldsets + (
        ('Student Info', {
            'fields': ('bio', 'phone', 'profile_picture', 'college_name', 'graduation_year')
        }),
    )