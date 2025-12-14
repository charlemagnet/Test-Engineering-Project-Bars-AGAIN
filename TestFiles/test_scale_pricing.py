import pytest
from itertools import product
# Import yolunu proje yapına uygun hale getirdim
from Engines.pricing_engine import calculate_dynamic_price, get_base_price

# --- Test Verisi Hazırlığı ---
classes = ["Yoga", "Boxing", "Fitness", "Basketball", "Tennis", "Swimming"]
hours = list(range(0, 24))  
member_types = ["Standard", "Premium", "Student"]

test_scenarios = list(product(classes, hours, member_types))

@pytest.mark.parametrize("class_type, hour, member_type", test_scenarios)
def test_pricing_all_combinations(class_type, hour, member_type):
    
    # --- 1. Beklenen Fiyatı Hesapla (Oracle Mantığı) ---
    base_price = get_base_price(class_type)
    
    # Zaman Çarpanı (Mevcut mantığı korudum)
    expected_time_multiplier = 1.0
    if 6 <= hour < 12:
        expected_time_multiplier = 0.8
    elif 17 <= hour < 24:
        expected_time_multiplier = 1.1
        
    # Üyelik Çarpanı (İstediğin yeni kurallar burada)
    expected_member_multiplier = 1.0
    
    if member_type == "Student":
        # %20 İndirim -> Fiyatın %80'ini öder
        expected_member_multiplier = 0.8
    elif member_type == "Premium":
        # %40 Zam -> Fiyatın %140'ını öder
        expected_member_multiplier = 1.4
    else:
        # Standard üye -> Fiyat sabit (1.0)
        expected_member_multiplier = 1.0
        
    # Beklenen nihai fiyat
    expected_price = round(base_price * expected_time_multiplier * expected_member_multiplier, 2)
    
    # --- 2. Fonksiyonu Çalıştır (Actual Result) ---
    actual_price = calculate_dynamic_price(class_type, hour, member_type)
    
    # --- 3. Karşılaştır (Assertion) ---
    # Not: Float hesaplamalarda bazen 0.0000001 gibi farklar olabilir, 
    # ama round(x, 2) kullandığımız için '==' genellikle yeterlidir.
    assert actual_price == expected_price, \
        f"HATA: {class_type} {hour}:00 {member_type} için beklenen {expected_price}, gelen {actual_price}"
    
    # --- 4. Mantıksal Kontroller (Sanity Checks) ---
    assert actual_price > 0  # Fiyat negatif olamaz

    # Fiyat Hiyerarşisi Kontrolü:
    # Aynı saat ve ders için; Student < Standard < Premium olmalı
    if member_type == "Student":
        standard_price = calculate_dynamic_price(class_type, hour, "Standard")
        assert actual_price < standard_price, "Öğrenci fiyatı standarttan düşük olmalı"
        
    if member_type == "Premium":
        standard_price = calculate_dynamic_price(class_type, hour, "Standard")
        assert actual_price > standard_price, "Premium fiyat standarttan yüksek olmalı"