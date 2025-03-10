from django.db import transaction
from .models import Train, Booking, User
from .enum import BookingStatus, BerthType


class BookingService:
    @staticmethod
    def allocate_berth(train, user):
        """Allocate appropriate berth based on user characteristics and availability"""
        if user.age < 5:
            return BerthType.NO_BERTH

        # Priority allocation for seniors
        if user.age >= 60 and train.lower_berths_available > 0:
            return BerthType.LOWER

        # Priority for ladies with children
        if user.gender == "Female" and train.lower_berths_available > 0:
            return BerthType.LOWER

        # Regular allocation
        if train.lower_berths_available > 0:
            return BerthType.LOWER
        if train.middle_berths_available > 0:
            return BerthType.MIDDLE
        if train.upper_berths_available > 0:
            return BerthType.UPPER

        return None

    @staticmethod
    @transaction.atomic
    def create_booking(user, train):
        """Create a booking with proper status and berth allocation"""

        # Lock the train record for atomic updates
        train = Train.objects.select_for_update().get(id=train.id)

        # Handle children under 5
        if user.age < 5:
            booking = Booking.objects.create(
                user=user,
                train=train,
                booking_status=BookingStatus.CONFIRMED.value,
                berth_type=BerthType.NO_BERTH.value,
                total_amount=0,
            )
            return booking

        # Try confirmed booking first
        if train.available_confirmed_berths > 0:
            berth_type = BookingService.allocate_berth(train, user)
            if berth_type:
                booking = Booking.objects.create(
                    user=user,
                    train=train,
                    booking_status=BookingStatus.CONFIRMED.value,
                    berth_type=berth_type.value,
                    total_amount=1000,  # Set appropriate amount
                )

                # Update berth availability
                train.available_confirmed_berths -= 1
                if berth_type == BerthType.LOWER:
                    train.lower_berths_available -= 1
                elif berth_type == BerthType.MIDDLE:
                    train.middle_berths_available -= 1
                elif berth_type == BerthType.UPPER:
                    train.upper_berths_available -= 1

                train.save()
                return booking

        # Try RAC if confirmed not available
        if train.available_rac_spots > 0:
            booking = Booking.objects.create(
                user=user,
                train=train,
                booking_status=BookingStatus.RAC.value,
                berth_type=BerthType.SIDE_LOWER.value,
                total_amount=1000,
            )
            train.available_rac_spots -= 1
            train.save()
            return booking

        # Try waiting list if RAC not available
        if train.waiting_list_count < 10:
            booking = Booking.objects.create(
                user=user,
                train=train,
                booking_status=BookingStatus.WAITING_LIST.value,
                berth_type=None,
                total_amount=1000,
            )
            train.waiting_list_count += 1
            train.save()
            return booking

        raise Exception("No tickets available")

    @staticmethod
    @transaction.atomic
    def cancel_booking(booking):
        """Handle booking cancellation and promotion of RAC/WL passengers"""
        train = Train.objects.select_for_update().get(id=booking.train.id)

        if booking.booking_status == BookingStatus.CONFIRMED.value:
            # Update berth availability
            train.available_confirmed_berths += 1
            if booking.berth_type == BerthType.LOWER.value:
                train.lower_berths_available += 1
            elif booking.berth_type == BerthType.MIDDLE.value:
                train.middle_berths_available += 1
            elif booking.berth_type == BerthType.UPPER.value:
                train.upper_berths_available += 1

            # Promote RAC passenger if any
            rac_booking = Booking.objects.filter(
                train=train, booking_status=BookingStatus.RAC.value
            ).first()

            if rac_booking:
                rac_booking.booking_status = BookingStatus.CONFIRMED.value
                rac_booking.berth_type = BookingService.allocate_berth(
                    train, rac_booking.user
                ).value
                rac_booking.save()

                train.available_rac_spots += 1

                # Promote waiting list passenger to RAC if any
                wl_booking = Booking.objects.filter(
                    train=train, booking_status=BookingStatus.WAITING_LIST.value
                ).first()

                if wl_booking:
                    wl_booking.booking_status = BookingStatus.RAC.value
                    wl_booking.berth_type = BerthType.SIDE_LOWER.value
                    wl_booking.save()
                    train.waiting_list_count -= 1

        train.save()
        booking.delete()
