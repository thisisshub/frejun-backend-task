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

# CoreFrejunConstraintsTest

This test suite (`CoreFrejunConstraintsTest`) is designed to validate the constraints and booking behavior in a train reservation system. It ensures that the train's capacity, RAC (Reservation Against Cancellation) limits, waiting list capacity, and special booking rules (like for children, senior citizens, and ladies with children) are adhered to correctly.

---

## Test Cases

### 1. **test_rac_capacity**

**Purpose:**  
This test verifies that the RAC (Reservation Against Cancellation) section can hold exactly 18 passengers (2 per berth for 9 berths).

**Steps:**

- First, it fills all 63 confirmed berths by creating bookings for 63 users.
- Then, it attempts to book 18 RAC tickets.
- It validates that all 18 RAC bookings have the status `RAC` and berth type as `SIDE_LOWER`.
- Finally, it asserts that no more RAC spots are available.

**Expected Outcome:**

- The 18 RAC bookings should succeed.
- Any further RAC bookings should not be possible as the limit is reached.

---

### 2. **test_waiting_list_limit**

**Purpose:**  
This test ensures that the waiting list is limited to only 10 tickets after all confirmed and RAC berths are booked.

**Steps:**

- Book 63 confirmed tickets to fill confirmed berths.
- Book 18 RAC tickets to fill RAC berths.
- Attempt to book 10 waiting list tickets, which should succeed.
- Attempt to book one more ticket, which should raise an exception with the message **"No tickets available"**.

**Expected Outcome:**

- Only 10 waiting list tickets can be booked.
- Booking an 11th waiting list ticket should raise an exception.

---

### 3. **test_child_booking**

**Purpose:**  
This test verifies that children under the age of 5 do not get any berth allocation.

**Steps:**

- Create a child user (age 4).
- Book a ticket for the child.
- Verify that the booking status is `CONFIRMED` but the berth type is `NO_BERTH`.
- Ensure that the berth availability is not reduced for a child booking.

**Expected Outcome:**

- Children under 5 should not occupy any berth.
- The confirmed berth count should remain unchanged.

---

### 4. **test_senior_citizen_priority**

**Purpose:**  
This test ensures that senior citizens (age 65 and above) get priority for lower berths.

**Steps:**

- Book 20 confirmed tickets, leaving one lower berth available.
- Book a ticket for a senior citizen (age 65).
- Validate that the senior citizen receives a `LOWER` berth.

**Expected Outcome:**

- Senior citizens should get priority for lower berths if available.

---

### 5. **test_lady_with_child_priority**

**Purpose:**  
This test ensures that ladies traveling with children get priority for lower berths.

**Steps:**

- Create a child and book a ticket for the child (age 4).
- Book 20 confirmed tickets, leaving one lower berth available.
- Book a ticket for the mother.
- Verify that the mother receives a `LOWER` berth.

**Expected Outcome:**

- Ladies traveling with children should get priority for lower berths.

---

### 6. **test_rac_berth_allocation**

**Purpose:**  
This test ensures that RAC passengers are allocated side-lower berths.

**Steps:**

- Book 63 confirmed tickets to fill all confirmed berths.
- Book one RAC ticket.
- Verify that the RAC passenger receives a `SIDE_LOWER` berth.

**Expected Outcome:**

- RAC passengers should always get a `SIDE_LOWER` berth.

---

### 7. **test_booking_progression**

**Purpose:**  
This test verifies the correct booking progression from **Confirmed** → **RAC** → **Waiting List**.

**Steps:**

- Book 63 confirmed tickets.
- Book 18 RAC tickets.
- Book 10 waiting list tickets.
- Validate the following:
  - No confirmed berths should be available.
  - No RAC spots should be available.
  - Waiting list should be exactly 10.

**Expected Outcome:**

- The booking system should transition through `CONFIRMED` → `RAC` → `WAITING LIST` correctly.
- Any further booking attempt should raise an exception.

---

## Summary

This test suite ensures that:

- The train's maximum capacity is strictly enforced (63 confirmed, 18 RAC, 10 waiting list).
- Special rules for children, senior citizens, and women with children are correctly applied.
- Booking progression and RAC behavior are consistent with real-world scenarios.

The constraints ensure that the system behaves as expected under maximum load and edge-case scenarios.
