from django.contrib import admin
from .models import EquipmentCategory, Location, Equipment, Booking, Notification

@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)

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