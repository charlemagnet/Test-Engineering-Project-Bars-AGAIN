import pytest
from hypothesis import given, strategies as st
from hypothesis import settings, Verbosity
from Engines.pricing_engine import calculate_dynamic_price

# Project modules
from Engines.refund_manager import calculate_refund
from Engines.reservation_system import ReservationSystem, GymClass

# --- PROPERTY 1: Refund Amount Boundary Invariant ---
# Refund never negative or exceed paid amount.
# Refund should be consistent with paid amount.

@settings(max_examples=200) # try 200 random scenarios
@given(
    class_type=st.sampled_from(["Yoga", "Boxing", "Fitness", "Basketball", "Tennis", "Swimming"]),
    paid_amount=st.floats(min_value=0.01, max_value=10000.0), # between 0.01 and 10,000
    days_before=st.floats(min_value=0.0, max_value=365.0)     # between 0 and 365 days
)
def test_prop_refund_boundaries(class_type, paid_amount, days_before):
    """
    Stress refund calculation boundaries.
    """
    # Action
    refund = calculate_refund(class_type, paid_amount, days_before)
    
    # Assertions / invariants
    
    # 1. Never negative
    assert refund >= 0.0, f"Negatif iade tespit edildi! Girdi: {paid_amount}, Gün: {days_before}"
    
    # 2. Never exceed paid amount
    # (Allow tiny float tolerance; refund <= paid)
    assert refund <= paid_amount + 0.0001, f"Ödenenden fazla iade! Refund: {refund}, Paid: {paid_amount}"

    # 3. Consistency: if >=2 days, full refund
    if days_before >= 2.0:
        assert refund == float(paid_amount)


# --- PROPERTY 2: Capacity Limit Invariant ---
# Bookings never exceed capacity.

@settings(max_examples=100)
@given(
    capacity=st.integers(min_value=1, max_value=50), # capacity between 1 and 50
    # generate random user IDs (may exceed capacity)
    user_ids=st.lists(st.integers(min_value=1), min_size=1, max_size=100) 
)
def test_prop_capacity_never_exceeded(capacity, user_ids):
    """
    Stress test for overbooking.
    """
    # Setup
    gym_class = GymClass("Hypothesis Test Class", "Yoga", capacity)
    rs = ReservationSystem()
    
    # Action: try booking users from user_ids
    successful_bookings = 0
    
    for uid in user_ids:
        try:
            # Assume each paid 100.0
            rs.book_class(uid, gym_class, paid_price=100.0)
            successful_bookings += 1
        except ValueError as e:
            # Expect 'Class is full' error (normal)
            assert str(e) == "Class is full"

    # Assertions / invariants
    
    # 1. booked <= capacity
    assert len(gym_class.booked_users) <= capacity
    
    # 2. booked <= attempted users
    assert len(gym_class.booked_users) <= len(user_ids)
    
    # 3. If unique users >= capacity, class must be full
    # (Assuming unique users; could use unique=True but simplified)
    unique_users = len(set(user_ids))
    if unique_users >= capacity:
        assert len(gym_class.booked_users) == capacity
    
@settings(max_examples=200)
@given(
    # Random Activities
    activity=st.sampled_from(["Yoga", "Boxing", "Fitness"]),
    # Random numbers
    hour=st.integers(min_value=-100, max_value=100),
    # Random membership
    member_type=st.sampled_from(["Standard", "Premium", "Student"])
)
def test_prop_hour_validation(activity, hour, member_type):
    """
    invalid 0 <= time <= 24
    """
    
    # 1: Valid times
    if 0 <= hour <= 23:
        price = calculate_dynamic_price(activity, hour, member_type)
        assert price > 0, "No error!"

    # 2 Invalid times
    else:
        with pytest.raises(ValueError):
            calculate_dynamic_price(activity, hour, member_type)