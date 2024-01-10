from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'region', 'age', 'phone', 'avatar', 'discount', 'is_staff', 'is_active')


admin.site.register(CustomUser, CustomUserAdmin)
