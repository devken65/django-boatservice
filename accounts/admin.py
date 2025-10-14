from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "username",
                    "password",
                    "name",
                    "email",
                    "is_host",
                    "gender",
                    "photo",
                ),
            },
        ),
        (
            "Important dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                ),
                "classes": ("collapse",),
            },
        ),
    )

    list_display = (
        # 반드시 model에서 존재하는 항목을 넣어줘야 함
        "username",
        "email",
        "name",
        "is_host",
    )
