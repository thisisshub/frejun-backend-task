from django.contrib import admin
from api.models import Booking, Route, Station, Train, User


class BookingAdmin(admin.ModelAdmin):
    list_display = ("booking_status", "booking_date", "total_amount", "user", "train")
    list_filter = ("booking_status", "booking_date", "total_amount", "user", "train")
    search_fields = (
        "id",
        "booking_status",
        "booking_date",
        "total_amount",
        "user",
        "train",
    )
    list_per_page = 10


class RouteAdmin(admin.ModelAdmin):
    list_display = ("source_station", "destination_station", "distance")
    list_filter = ("source_station", "destination_station", "distance")
    search_fields = ("id", "source_station", "destination_station", "distance")
    list_per_page = 10


class TrainAdmin(admin.ModelAdmin):
    list_display = ("train_name", "train_number", "route")
    list_filter = ("train_name", "train_number", "route")
    search_fields = ("id", "train_name", "train_number", "route")
    list_per_page = 10


class UserAdmin(admin.ModelAdmin):
    list_display = ("name", "age", "gender", "is_child")
    list_filter = ("name", "age", "gender", "is_child")
    search_fields = ("id", "name", "age", "gender", "is_child")
    list_per_page = 10


class StationAdmin(admin.ModelAdmin):
    list_display = ("station_name", "station_code")
    list_filter = ("station_name", "station_code")
    search_fields = ("station_name", "station_code")
    list_per_page = 10


admin.site.register(User, UserAdmin)
admin.site.register(Train, TrainAdmin)
admin.site.register(Route, RouteAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Station, StationAdmin)
