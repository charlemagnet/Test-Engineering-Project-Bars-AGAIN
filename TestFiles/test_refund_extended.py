import pytest
from pytest import approx
# Import yolunu proje yapına uygun olduğundan emin ol
from Engines.refund_manager import calculate_refund 

# --- Equivalent Partitioning & Boundary Value Tests for Cancellation Time ---

# Test data format: (Class Type, Days Before Cancellation, Expected Refund Percentage)
@pytest.mark.parametrize("class_type, days_before, expected_refund_rate", [
    # 1. Early Cancellation (Days Before >= 2) - Full Refund (100.0%)
    ("Yoga", 3, 100.0),      # Standard early cancellation
    ("Boxing", 2.1, 100.0),  # Just over the 2-day threshold
    ("Fitness", 100, 100.0), # Extremely early cancellation
    
    # 2. Late Cancellation (Days Before < 2) - Specific Class Policy (README Rules)
    ("Yoga", 1.9, 30.0),     # Just below 2 days -> Yoga policy: 30%
    ("Boxing", 1.0, 50.0),   # Late cancellation -> Boxing policy: 50%
    ("Fitness", 0.5, 10.0),  # Late cancellation -> Fitness policy: 10%
    ("Basketball", 1.5, 40.0), # Late cancellation -> Basketball policy: 40%
    ("Tennis", 0.01, 80.0),  # Near-miss -> Tennis policy: 80%
    ("Swimming", 1.5, 15.0), # Late cancellation -> Swimming policy: 15%
    
    # 3. Exact Boundary Test (2.0 Days Before)
    ("Yoga", 2.0, 100.0),    # Exact boundary should yield full refund
    ("Boxing", 2.0, 100.0),  # Exact boundary check for another class
])
def test_refund_policy_time_and_type(class_type, days_before, expected_refund_rate):
    """Tests the refund percentage based on cancellation time and class type."""
    paid_amount = 500.0 # Standard payment amount for calculation
    
    # Act
    refund_amount = calculate_refund(class_type, paid_amount, days_before)
    
    # Assert
    expected_amount = paid_amount * (expected_refund_rate / 100)
    # Using approx for safe float comparison
    assert refund_amount == approx(expected_amount), \
        f"{class_type} dersi {days_before} gün kala iptal edildiğinde beklenen {expected_amount}, gelen {refund_amount}"

def test_refund_for_zero_paid_amount():
    """Tests that the refund amount is zero if no payment was made."""
    paid_amount = 0.0
    days_before = 3 # Should be 100% refund rate
    refund_amount = calculate_refund("Yoga", paid_amount, days_before)
    assert refund_amount == 0.0

def test_refund_for_non_existent_class():
    """Tests an invalid class type. Should raise KeyError."""
    # Assuming the system raises KeyError for unknown types (Strict Validation)
    with pytest.raises(KeyError): 
        calculate_refund("NonExistentClass", 100.0, 1.0)