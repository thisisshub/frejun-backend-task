import factory
from factory.django import DjangoModelFactory
from api.models import User, Station, Route, Train, Booking
from api.enum import BookingStatus, BerthType

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    name = factory.Faker('name')
    age = factory.Faker('random_int', min=18, max=80)
    gender = factory.Iterator(['Male', 'Female'])
    is_child = False

class StationFactory(DjangoModelFactory):
    class Meta:
        model = Station

    station_name = factory.Sequence(lambda n: f'Station {n}')
    station_code = factory.Sequence(lambda n: f'ST{n}')

class RouteFactory(DjangoModelFactory):
    class Meta:
        model = Route

    source_station = factory.SubFactory(StationFactory)
    destination_station = factory.SubFactory(StationFactory)
    distance = factory.Faker('random_int', min=100, max=2000)
    intermediate_stations = factory.LazyFunction(lambda: {})

class TrainFactory(DjangoModelFactory):
    class Meta:
        model = Train

    train_name = factory.Sequence(lambda n: f'Train {n}')
    train_number = factory.Sequence(lambda n: f'TR{n}')
    route = factory.SubFactory(RouteFactory)
    
    # Default berth values
    total_confirmed_berths = 63
    total_rac_berths = 9
    available_confirmed_berths = 63
    available_rac_spots = 18
    waiting_list_count = 0
    lower_berths_available = 21
    middle_berths_available = 21
    upper_berths_available = 21
    side_lower_berths_available = 9
    side_upper_berths_available = 9

class BookingFactory(DjangoModelFactory):
    class Meta:
        model = Booking

    user = factory.SubFactory(UserFactory)
    train = factory.SubFactory(TrainFactory)
    booking_status = BookingStatus.CONFIRMED.value
    berth_type = BerthType.LOWER.value
    total_amount = factory.Faker('pydecimal', left_digits=4, right_digits=2, positive=True)
    
