from django.contrib import admin

from .models import Account, Profile


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
