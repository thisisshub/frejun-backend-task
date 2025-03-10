from django.urls import path
from api.views import (
    UserView,
    StationView,
    RouteView,
    TrainView,
    BookingView,
)

urlpatterns = [
    path("user/", UserView.as_view(), name="user"),
    path("station/", StationView.as_view(), name="station"),
    path("route/", RouteView.as_view(), name="route"),
    path("train/", TrainView.as_view(), name="train"),
    path("booking/", BookingView.as_view(), name="booking"),
]