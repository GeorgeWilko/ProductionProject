from django.contrib import admin
from django.utils.html import format_html

from .models import EquipmentCategory, Location, Equipment, Booking, Notification


@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "image_thumb")
    search_fields = ("name",)

    def image_thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:45px;width:auto;border-radius:4px;" />', obj.image.url)
        return "—"

    image_thumb.short_description = "Image"


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "country")
    search_fields = ("name", "city", "country")
    list_filter = ("city", "country")


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "category", "location", "quantity")
    list_filter = ("status", "category", "location")
    search_fields = ("name", "description")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "equipment", "status", "start_date", "end_date", "created_at")
    list_filter = ("status", "start_date", "end_date")
    search_fields = ("user__username", "equipment__name")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "booking", "created_at")
    search_fields = ("user__username", "booking__equipment__name", "message")
