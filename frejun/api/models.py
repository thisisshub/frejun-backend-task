from uuid import uuid4
from django.db import models
from api.enum import BookingStatus, BerthType


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(BaseModel):
    age = models.PositiveIntegerField()
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=255)
    is_child = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Station(models.Model):
    station_name = models.CharField(max_length=255)
    station_code = models.CharField(max_length=255, primary_key=True)

    def __str__(self):
        return self.station_name


class Route(BaseModel):
    distance = models.PositiveIntegerField()
    source_station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="source_station"
    )
    destination_station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="destination_station"
    )
    intermediate_stations = models.JSONField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.source_station.station_name} to {self.destination_station.station_name}"


class Train(BaseModel):
    train_name = models.CharField(max_length=255)
    train_number = models.CharField(max_length=255)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="route")

    # Berth availability tracking
    total_confirmed_berths = models.PositiveIntegerField(default=63)
    total_rac_berths = models.PositiveIntegerField(default=9)
    available_confirmed_berths = models.PositiveIntegerField(default=63)
    available_rac_spots = models.PositiveIntegerField(default=18)  # 2 per RAC berth
    waiting_list_count = models.PositiveIntegerField(default=0)

    # Track different berth types
    lower_berths_available = models.PositiveIntegerField(default=21)
    middle_berths_available = models.PositiveIntegerField(default=21)
    upper_berths_available = models.PositiveIntegerField(default=21)
    side_lower_berths_available = models.PositiveIntegerField(default=9)  # RAC berths
    side_upper_berths_available = models.PositiveIntegerField(default=9)  # RAC berths

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(waiting_list_count__lte=10), name="max_waiting_list_10"
            )
        ]


class Booking(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    train = models.ForeignKey(Train, on_delete=models.CASCADE, related_name="train")
    booking_status = models.CharField(
        max_length=255,
        choices=[(status.value, status.name) for status in BookingStatus],
        null=True,
        blank=True,
    )
    berth_type = models.CharField(
        max_length=255,
        choices=[(berth.value, berth.name) for berth in BerthType],
        null=True,
        blank=True,
    )
    booking_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
