import pytest
from datetime import datetime, timedelta
# Assuming refund_manager contains the refund logic
#from refund_manager import calculate_refund 
from pytest import approx

# --- Equivalent Partitioning & Boundary Value Tests for Cancellation Time ---

# Test data format: (Class Type, Days Before Cancellation, Expected Refund Percentage)
@pytest.mark.parametrize("class_type, days_before, expected_refund_rate", [
    # 1. Early Cancellation (Days Before > 2) - Full Refund (100.0%)
    ("Yoga", 3, 100.0),      # Standard early cancellation
    ("Boxing", 2.1, 100.0),  # Just over the 2-day threshold
    ("Fitness", 100, 100.0), # Extremely early cancellation
    
    # 2. Late Cancellation (Days Before < 2) - Specific Class Policy
    ("Yoga", 1.9, 30.0),     # Just below the 2-day threshold (Yoga: 30%)
    ("Boxing", 1.0, 50.0),   # Late cancellation for Boxing (50%)
    ("Fitness", 0.5, 10.0),  # Very late cancellation for Fitness (10%)
    ("Tennis", 0.01, 80.0),  # Near-miss cancellation for Tennis (80%)
    ("Swimming", 1.5, 15.0), # Late cancellation for Swimming (15%)
    
    # 3. Exact Boundary Test (2.0 Days Before)
    ("Yoga", 2.0, 100.0),    # Exact boundary should yield full refund
    ("Boxing", 2.0, 100.0),  # Exact boundary check for another class
])
def test_refund_policy_time_and_type(class_type, days_before, expected_refund_rate):
    """Tests the refund percentage based on cancellation time and class type."""
    paid_amount = 500.0 # Standard payment amount for calculation
    refund_amount = calculate_refund(class_type, paid_amount, days_before)
    
    expected_amount = paid_amount * (expected_refund_rate / 100)
    # Using approx for safe float comparison
    assert refund_amount == approx(expected_amount)

def test_refund_for_zero_paid_amount():
    """Tests that the refund amount is zero if no payment was made."""
    paid_amount = 0.0
    days_before = 3 # Should be 100% refund rate
    refund_amount = calculate_refund("Yoga", paid_amount, days_before)
    assert refund_amount == 0.0

def test_refund_for_non_existent_class():
    """Tests an invalid class type. Should default to a minimum policy or raise an error."""
    # Assuming the system defaults to 0% refund or raises ValueError for unknown types
    with pytest.raises(KeyError): # Or another specific exception like ValueError
        calculate_refund("NonExistentClass", 100.0, 1.0)