import pytest
from Engines.pricing_engine import calculate_dynamic_price, get_base_price

# --- PAIRWISE TEST VERİLERİ ---
# Format: (Activity, Hour, Membership, Expected_Result)
# Beklenen sonuçları formüle göre hesapladık: Base * TimeMult * MemMult
pairwise_data = [
    # 1. Yoga (Base 200) | Morning (0.8) | Standard (1.0) -> 160.0
    ("Yoga", 9, "Standard", 160.0),
    
    # 2. Yoga (Base 200) | Day (1.0) | Premium (1.4) -> 280.0
    ("Yoga", 14, "Premium", 280.0),
    
    # 3. Boxing (Base 120) | Evening (1.1) | Standard (1.0) -> 132.0
    ("Boxing", 19, "Standard", 132.0),
    
    # 4. Fitness (Base 80) | Morning (0.8) | Student (0.8) -> 51.2
    ("Fitness", 9, "Student", 51.2),
    
    # 5. Basketball (Base 40) | Day (1.0) | Standard (1.0) -> 40.0
    ("Basketball", 14, "Standard", 40.0),
    
    # 6. Tennis (Base 90) | Evening (1.1) | Premium (1.4) -> 138.6
    ("Tennis", 19, "Premium", 138.6),
    
    # 7. Swimming (Base 30) | Morning (0.8) | Premium (1.4) -> 33.6
    ("Swimming", 9, "Premium", 33.6),
    
    # 8. Boxing (Base 120) | Day (1.0) | Student (0.8) -> 96.0
    ("Boxing", 14, "Student", 96.0),
    
    # 9. Fitness (Base 80) | Evening (1.1) | Premium (1.4) -> 123.2
    ("Fitness", 19, "Premium", 123.2),
    
    # 10. Swimming (Base 30) | Day (1.0) | Standard (1.0) -> 30.0
    ("Swimming", 14, "Standard", 30.0)
]

@pytest.mark.parametrize("activity, hour, membership, expected_price", pairwise_data)
def test_pairwise_pricing_combinations(activity, hour, membership, expected_price):
    """
    Bu test, 'allpairspy' aracı ile üretilen İkili (Pairwise) test setini uygular.
    Amaç: Minimum test sayısı ile tüm parametre çiftlerini (Activity-Hour, Activity-Member, Hour-Member) kapsamaktır.
    """
    # Act (Eylem)
    actual_price = calculate_dynamic_price(activity, hour, membership)
    
    assert actual_price == pytest.approx(expected_price, 0.01), \
        f"HATA: {activity} | {hour}:00 | {membership} -> Beklenen: {expected_price}, Gelen: {actual_price}"