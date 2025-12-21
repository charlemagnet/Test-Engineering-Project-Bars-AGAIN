import pytest
from Engines.reservation_system import ReservationSystem, GymClass

def test_formal_precondition_enforcement():
    """
    This test verifies that the precondition in the book_class method
    is properly enforced. If we try to book a class that is already at
    """
    gym_class = GymClass("Formal Test Class", "Yoga", capacity=1)
    rs = ReservationSystem()

    # 1. Setup: Fill the class to capacity
    rs.book_class(101, gym_class, 100.0)
    
    # 2. Test: Try to book one more user, which should violate the precondition
    with pytest.raises(AssertionError) as excinfo:
        rs.book_class(102, gym_class, 100.0)
    
    assert "Precondition Failed" in str(excinfo.value)

def test_formal_invariant_maintenance():
    """
    This test verifies that the invariant in the book_class method
    is properly maintained.
    """
    gym_class = GymClass("Invariant Class", "Boxing", capacity=5)
    rs = ReservationSystem()
    
    gym_class.booked_users = [1, 2, 3, 4, 5] 
    
    # Attempt to book another user, which should violate the invariant
    with pytest.raises(AssertionError) as excinfo:
        rs.book_class(999, gym_class, 100.0)
        
    assert "Precondition Failed" in str(excinfo.value)