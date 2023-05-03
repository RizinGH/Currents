from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm

from .models import *

User = get_user_model()

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'password', 'is_staff', 'is_superuser')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser'),
        }),
    )
    add_fieldsets = (
        (None, {'fields': ('email' 'password1', 'password2')}),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser'),
        }),
    )

    search_fields = ('email', 'username',)
    ordering = ('email',)
    filter_horizontal = ()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)

# Register your models here.
admin.site.register(User)
admin.site.register(UserDetails)
admin.site.register(Subscription)
admin.site.register(Favourites)
admin.site.register(Report)
admin.site.register(Feedback)
