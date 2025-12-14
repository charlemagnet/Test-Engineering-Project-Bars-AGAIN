import pytest
# Assuming reservation_system contains the reservation logic and GymClass
from Engines.reservation_system import ReservationSystem, GymClass 

@pytest.fixture
def reservation_system():
    """Fixture to set up a clean ReservationSystem for each test."""
    return ReservationSystem()

@pytest.fixture
def yoga_class():
    """Fixture for a standard Yoga class with capacity 50."""
    return GymClass(name="Yoga Flow", type="Yoga", capacity=50)

@pytest.fixture
def small_class():
    """Fixture for a small capacity class (e.g., Tennis) with capacity 5."""
    return GymClass(name="Private Tennis", type="Tennis", capacity=5)

# --- Successful Reservation Tests ---

def test_make_successful_reservation(reservation_system, yoga_class):
    """Tests a standard successful reservation and verifies occupancy increase."""
    user_id = 101
    result = reservation_system.book_class(user_id, yoga_class)
    
    assert result["status"] == "confirmed"
    assert yoga_class.current_occupancy == 1
    assert user_id in yoga_class.reserved_users

def test_multiple_successful_reservations(reservation_system, yoga_class):
    """Tests booking multiple distinct users to the same class."""
    users = [201, 202, 203]
    for user_id in users:
        reservation_system.book_class(user_id, yoga_class)
    
    assert yoga_class.current_occupancy == 3
    for user_id in users:
        assert user_id in yoga_class.reserved_users

# --- Boundary and Capacity Tests ---

def test_capacity_at_limit_success(reservation_system, small_class):
    """Tests booking successfully when capacity is at the boundary limit (N-1 -> N)."""
    # Fill up the class to N-1
    for i in range(1, small_class.capacity):
        reservation_system.book_class(i, small_class) 
        
    last_user_id = 100
    result = reservation_system.book_class(last_user_id, small_class)
    
    assert result["status"] == "confirmed"
    assert small_class.current_occupancy == small_class.capacity
    assert last_user_id in small_class.reserved_users

def test_capacity_overflow_raises_error(reservation_system, small_class):
    """Tests that booking when capacity is full raises an error (N+1 case)."""
    # Fill up the class completely (N)
    for i in range(1, small_class.capacity + 1):
        reservation_system.book_class(i, small_class) 
        
    overflow_user_id = 999
    
    # Expecting an error (Red) because the class is full
    with pytest.raises(ValueError, match="Class is full"):
        reservation_system.book_class(overflow_user_id, small_class)

# --- Double Booking and Cancellation Tests ---

def test_prevent_double_booking_raises_error(reservation_system, yoga_class):
    """Ensures the same user cannot book the same class twice."""
    user_id = 301
    reservation_system.book_class(user_id, yoga_class) # First successful booking
    
    # Second booking attempt by the same user
    with pytest.raises(ValueError, match="Already booked"):
        reservation_system.book_class(user_id, yoga_class)
    
    # Occupancy must still be 1
    assert yoga_class.current_occupancy == 1

def test_successful_cancellation(reservation_system, yoga_class):
    """Tests if a reservation can be cancelled and capacity is freed up."""
    user_id = 401
    reservation_system.book_class(user_id, yoga_class)
    assert yoga_class.current_occupancy == 1

    # Cancel the booking
    cancel_result = reservation_system.cancel_booking(user_id, yoga_class)
    
    assert cancel_result["status"] == "cancelled"
    assert yoga_class.current_occupancy == 0
    assert user_id not in yoga_class.reserved_users