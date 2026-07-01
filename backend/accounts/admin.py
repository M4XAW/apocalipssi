"""Administration des demandes d'accès aux données (SAR)."""

from django.contrib import admin

from .models import DataRequest, Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "email_verified", "created_at")
    search_fields = ("user__email", "user__username")
    readonly_fields = ("created_at",)


@admin.register(DataRequest)
class DataRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "request_type",
        "status",
        "export_format",
        "requested_at",
        "responded_at",
    )
    list_filter = ("status", "request_type", "export_format")
    search_fields = ("user__email", "user__username", "export_file_hash")
    readonly_fields = (
        "user",
        "request_type",
        "status",
        "export_format",
        "export_file_hash",
        "requested_at",
        "responded_at",
    )
    ordering = ("-requested_at",)
