from django.contrib import admin
from members.models import CustomUser, Subscription


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email',]


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    pass
