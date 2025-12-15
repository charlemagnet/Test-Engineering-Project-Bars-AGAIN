import pytest
from Engines.pricing_engine import calculate_dynamic_price, get_base_price

# Karar Tablosundaki (Decision Table) kuralları test verisine dönüştürüyoruz
# Format: (Kural ID, Aktivite, Saat, Üyelik Tipi, Beklenen Çarpan)
decision_table_data = [
    ("R1", "Yoga", 9,  "Standard", 0.8 * 1.0),  # Sabah + Std
    ("R2", "Yoga", 9,  "Student",  0.8 * 0.8),  # Sabah + Ogr
    ("R3", "Yoga", 9,  "Premium",  0.8 * 1.4),  # Sabah + Pre
    ("R4", "Yoga", 14, "Standard", 1.0 * 1.0),  # Gunduz + Std
    ("R5", "Yoga", 14, "Student",  1.0 * 0.8),  # Gunduz + Ogr
    ("R6", "Yoga", 14, "Premium",  1.0 * 1.4),  # Gunduz + Pre
    ("R7", "Yoga", 19, "Standard", 1.1 * 1.0),  # Aksam + Std
    ("R8", "Yoga", 19, "Student",  1.1 * 0.8),  # Aksam + Ogr
    ("R9", "Yoga", 19, "Premium",  1.1 * 1.4),  # Aksam + Pre
]

@pytest.mark.parametrize("rule_id, activity, hour, member_type, expected_mult", decision_table_data)
def test_pricing_decision_table(rule_id, activity, hour, member_type, expected_mult):
    """
    Bu test, Karar Tablosundaki (R1-R9) her bir kuralı doğrular.
    """
    # 1. Beklenen Fiyatı Hesapla
    base_price = get_base_price(activity)
    expected_price = round(base_price * expected_mult, 2)
    
    # 2. Gerçek Fiyatı Al
    actual_price = calculate_dynamic_price(activity, hour, member_type)
    
    # 3. Karşılaştır
    assert actual_price == expected_price, f"Kural {rule_id} başarısız oldu!"