from api.models import Booking
from api.services import BookingService
from rest_framework.test import APIClient
from rest_framework.test import APITestCase
from api.enum import BookingStatus, BerthType
from api.factory import (
    UserFactory,
    TrainFactory,
)


class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()


class UserViewTest(BaseAPITestCase):
    def test_user_creation(self):
        user = UserFactory.build()
        response = self.client.post(
            "/api/v1/user/", {"name": user.name, "age": user.age, "gender": user.gender}
        )
        self.assertEqual(response.status_code, 201)

    def test_user_creation_with_child(self):
        user = UserFactory.build(age=4)
        response = self.client.post(
            "/api/v1/user/", {"name": user.name, "age": user.age, "gender": user.gender}
        )
        assert response.data["is_child"] == True
        assert response.status_code == 201


class BookingViewTest(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.user = UserFactory.create()
        self.train = TrainFactory.create()

    def test_booking_creation(self):
        # Verify train was created properly
        self.assertIsNotNone(self.train.id)
        self.assertIsNotNone(self.train.route)
        self.assertIsNotNone(self.train.route.source_station)
        self.assertIsNotNone(self.train.route.destination_station)

        # Create booking through service
        booking = BookingService.create_booking(self.user, self.train)

        # Verify booking was created
        self.assertIsNotNone(booking)
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.train, self.train)
        self.assertEqual(booking.booking_status, BookingStatus.CONFIRMED.value)

        # Verify train stats were updated
        self.train.refresh_from_db()
        self.assertEqual(self.train.available_confirmed_berths, 62)

    def test_booking_api(self):
        response = self.client.post(
            "/api/v1/booking/",
            {
                "user": str(self.user.id),
                "train": str(self.train.id),
                "total_amount": "1000.00",
            },
        )
        self.assertEqual(response.status_code, 201)

        # Verify booking was created in DB
        booking = Booking.objects.get(id=response.data["id"])
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.train, self.train)

    def test_rac_booking(self):
        # Fill all confirmed berths except one
        for _ in range(62):
            user = UserFactory.create()
            BookingService.create_booking(user, self.train)

        # Create one more booking
        user = UserFactory.create()
        booking = BookingService.create_booking(user, self.train)

        # This should be the last confirmed booking
        self.assertEqual(booking.booking_status, BookingStatus.CONFIRMED.value)

        # Next booking should be RAC
        user = UserFactory.create()
        booking = BookingService.create_booking(user, self.train)
        self.assertEqual(booking.booking_status, BookingStatus.RAC.value)
        self.assertEqual(booking.berth_type, BerthType.SIDE_LOWER.value)

    def test_waiting_list_booking(self):
        # Fill all confirmed berths
        for _ in range(63):
            user = UserFactory.create()
            BookingService.create_booking(user, self.train)

        # Fill all RAC spots
        for _ in range(18):
            user = UserFactory.create()
            booking = BookingService.create_booking(user, self.train)
            self.assertEqual(booking.booking_status, BookingStatus.RAC.value)

        # Next booking should be waiting list
        user = UserFactory.create()
        booking = BookingService.create_booking(user, self.train)
        self.assertEqual(booking.booking_status, BookingStatus.WAITING_LIST.value)
        self.assertIsNone(booking.berth_type)


class CoreFrejunConstraintsTest(BaseAPITestCase):
    def setUp(self):
        super().setUp()
        self.train = TrainFactory.create()

    def test_rac_capacity(self):
        """Test that RAC can hold exactly 18 passengers (2 per berth for 9 berths)"""
        # Fill all confirmed berths first
        for _ in range(63):
            user = UserFactory.create()
            BookingService.create_booking(user, self.train)

        # Try to book 18 RAC tickets
        for _ in range(18):
            user = UserFactory.create()
            booking = BookingService.create_booking(user, self.train)
            self.assertEqual(booking.booking_status, BookingStatus.RAC.value)
            self.assertEqual(booking.berth_type, BerthType.SIDE_LOWER.value)

        # Verify RAC is full
        self.train.refresh_from_db()
        self.assertEqual(self.train.available_rac_spots, 0)

    def test_waiting_list_limit(self):
        """Test that waiting list is limited to 10 tickets"""
        # Fill all confirmed berths
        for _ in range(63):
            user = UserFactory.create()
            BookingService.create_booking(user, self.train)

        # Fill all RAC spots
        for _ in range(18):
            user = UserFactory.create()
            BookingService.create_booking(user, self.train)

        # Book 10 waiting list tickets
        for _ in range(10):
            user = UserFactory.create()
            booking = BookingService.create_booking(user, self.train)
            self.assertEqual(booking.booking_status, BookingStatus.WAITING_LIST.value)

        # Try to book one more ticket
        user = UserFactory.create()
        with self.assertRaises(Exception) as context:
            BookingService.create_booking(user, self.train)
        self.assertTrue("No tickets available" in str(context.exception))

    def test_child_booking(self):
        """Test that children under 5 don't get berth allocation"""
        # Create a child user
        child = UserFactory.create(age=4, is_child=True)
        booking = BookingService.create_booking(child, self.train)

        # Verify booking details
        self.assertEqual(booking.booking_status, BookingStatus.CONFIRMED.value)
        self.assertEqual(booking.berth_type, BerthType.NO_BERTH.value)

        # Verify berth count wasn't affected
        self.train.refresh_from_db()
        self.assertEqual(self.train.available_confirmed_berths, 63)
        self.assertEqual(self.train.lower_berths_available, 21)

    def test_senior_citizen_priority(self):
        """Test that seniors get priority for lower berths"""
        # Fill most lower berths, leaving just one
        for _ in range(20):
            user = UserFactory.create()
            BookingService.create_booking(user, self.train)

        # Book for a senior citizen
        senior = UserFactory.create(age=65)
        booking = BookingService.create_booking(senior, self.train)

        # Verify they got a lower berth
        self.assertEqual(booking.berth_type, BerthType.LOWER.value)
        self.assertEqual(booking.booking_status, BookingStatus.CONFIRMED.value)

    def test_lady_with_child_priority(self):
        """Test that ladies with children get priority for lower berths"""
        # Create a mother
        mother = UserFactory.create(gender="Female")

        # Create and book for her child first
        child = UserFactory.create(age=4, is_child=True)
        child_booking = BookingService.create_booking(child, self.train)

        # Fill most lower berths, leaving just one
        for _ in range(20):
            user = UserFactory.create()
            BookingService.create_booking(user, self.train)

        # Book for the mother
        mother_booking = BookingService.create_booking(mother, self.train)

        # Verify she got a lower berth
        self.assertEqual(mother_booking.berth_type, BerthType.LOWER.value)
        self.assertEqual(mother_booking.booking_status, BookingStatus.CONFIRMED.value)

    def test_rac_berth_allocation(self):
        """Test that RAC passengers are allocated side-lower berths"""
        # Fill all confirmed berths
        for _ in range(63):
            user = UserFactory.create()
            BookingService.create_booking(user, self.train)

        # Book an RAC ticket
        user = UserFactory.create()
        booking = BookingService.create_booking(user, self.train)

        # Verify berth allocation
        self.assertEqual(booking.booking_status, BookingStatus.RAC.value)
        self.assertEqual(booking.berth_type, BerthType.SIDE_LOWER.value)

    def test_booking_progression(self):
        """Test the progression from Confirmed -> RAC -> Waiting List"""
        bookings = []

        # Book all confirmed berths
        for _ in range(63):
            user = UserFactory.create()
            booking = BookingService.create_booking(user, self.train)
            self.assertEqual(booking.booking_status, BookingStatus.CONFIRMED.value)
            bookings.append(booking)

        # Book all RAC spots
        for _ in range(18):
            user = UserFactory.create()
            booking = BookingService.create_booking(user, self.train)
            self.assertEqual(booking.booking_status, BookingStatus.RAC.value)
            bookings.append(booking)

        # Book all waiting list spots
        for _ in range(10):
            user = UserFactory.create()
            booking = BookingService.create_booking(user, self.train)
            self.assertEqual(booking.booking_status, BookingStatus.WAITING_LIST.value)
            bookings.append(booking)

        # Verify final counts
        self.train.refresh_from_db()
        self.assertEqual(self.train.available_confirmed_berths, 0)
        self.assertEqual(self.train.available_rac_spots, 0)
        self.assertEqual(self.train.waiting_list_count, 10)
