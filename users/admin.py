from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'email',
        'phone',
        'is_active',
        'created_at',
    )
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
    )
    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
        'phone',
    )
    ordering = (
        '-created_at',
    )
    readonly_fields = (
        'created_at',
    )

    fieldsets = (
        (
            None, {
                'fields': (
                    'username',
                    'password',
                )
            }
         ),
        (
            'Personal Info', {
                'fields': (
                    'first_name',
                    'last_name',
                    'email',
                    'phone',
                )
            }
        ),
        (
            'Permissions', {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                )
            }
        ),
        (
            'Important Dates', {
                'fields': (
                    'last_login',
                    'created_at',
                )
            }
        ),
    )

    add_fieldsets = (
        (
            None, {
                'classes': (
                    'wide',
                ),
                'fields': (
                    'username',
                    'first_name',
                    'last_name',
                    'email',
                    'phone',
                    'password1',
                    'password2',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
    )
