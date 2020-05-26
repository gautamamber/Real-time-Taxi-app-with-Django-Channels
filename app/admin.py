from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from . import models


@admin.register(models.User)
class UserAdmin(DefaultUserAdmin):
    """
    Representation in django admin panel
    """
    pass


@admin.register(models.Trip)
class TripAdmin(admin.ModelAdmin):
    """
    Representation in django admin panel
    """
    fields = (
        'id', 'pick_up_address', 'drop_off_address', 'status',
        'driver', 'rider',
        'created', 'updated',
    )
    list_display = (
        'id', 'pick_up_address', 'drop_off_address', 'status',
        'driver', 'rider',
        'created', 'updated',
    )
    list_filter = (
        'status',
    )
    readonly_fields = (
        'id', 'created', 'updated',
    )
