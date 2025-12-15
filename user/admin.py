# admin.py
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """Customize how CustomUser is displayed in Django admin."""

    model = CustomUser
    list_display = (
        "username",
        "email",
        "phone_number",
        "role",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("role", "is_staff", "is_superuser")
    ordering = ("email",)
    search_fields = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password", "phone_number")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Role info", {"fields": ("role",)}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "phone_number",
                    "password1",
                    "password2",
                    "role",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
