# Railway Booking System

A Django-based railway booking system that implements complex seat allocation logic including confirmed berths, RAC (Reservation Against Cancellation), and waiting list management.

## Features

- **Berth Management**:
  - 63 confirmed berths
  - 9 RAC berths (accommodating 18 passengers, 2 per side-lower berth)
  - 10 waiting-list tickets maximum

- **Priority Allocation**:
  - Senior citizens (60+) get priority for lower berths
  - Ladies with children get priority for lower berths
  - Children under 5 don't get berth allocation but are recorded

- **Booking States**:
  - Confirmed
  - RAC (Reservation Against Cancellation)
  - Waiting List

## Models

### User
- Basic user information (name, age, gender)
- Child status tracking
- Booking history

### Train
- Berth availability tracking
- RAC and waiting list counters
- Different berth type availability

### Booking
- Links users and trains
- Tracks booking status and berth type
- Handles booking amount

## Business Logic

The booking system implements these core rules:

1. **Berth Allocation**:
   - First 63 bookings get confirmed status
   - Next 18 bookings get RAC status
   - Next 10 bookings go to waiting list
   - Further bookings are rejected

2. **Priority System**:
   - Seniors (60+) get priority for lower berths
   - Ladies with children get priority for lower berths
   - Regular passengers get any available berth

3. **RAC Handling**:
   - RAC passengers share side-lower berths
   - When confirmed passengers cancel, RAC gets promoted
   - When RAC gets promoted, waiting list moves to RAC

## Constraints Test

The constraints test is designed to ensure that the booking system adheres to the defined business logic and rules. It verifies the following:

1. **Berth Allocation Limits**:
   - Ensures that no more than 63 bookings are confirmed.
   - Ensures that no more than 18 bookings are assigned RAC status.
   - Ensures that no more than 10 bookings are placed on the waiting list.

2. **Priority Allocation**:
   - Tests that senior citizens and ladies with children are prioritized for lower berths.
   - Validates that regular passengers are allocated any available berth only after priority passengers.

3. **RAC Promotion**:
   - Confirms that when a confirmed booking is canceled, the next passenger in the RAC list is promoted to confirmed status.
   - Ensures that the waiting list is correctly updated when a RAC passenger is promoted.

The constraints test is executed through a series of unit tests that simulate various booking scenarios, ensuring that the system behaves as expected under different conditions.
