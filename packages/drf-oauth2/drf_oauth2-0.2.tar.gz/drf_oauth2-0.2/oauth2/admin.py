from django.contrib import admin

from oauth2.models import UserData
from oauth2.utils import get_admin_model

ModelAdmin = get_admin_model(name="unfold")


@admin.register(UserData)
class AuditLogAdmin(ModelAdmin):
    list_display = ("id", "user", "provider", "uid", "created_at")
    search_fields = ("provider", "uid")
    list_filter = ("provider",)
    autocomplete_fields = ("user",)
