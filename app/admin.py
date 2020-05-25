from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from . import models


@admin.register(models.User)
class UserAdmin(DefaultUserAdmin):
    """
    Representation in django admin panel
    """
    pass
