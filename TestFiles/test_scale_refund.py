import pytest
from Engines.refund_manager import calculate_refund

class_types = ["Yoga", "Boxing", "Fitness", "Basketball", "Tennis", "Swimming"]

# 0.0 günden 3.0 güne kadar 0.5 aralıklarla test verisi üret
days_to_test = [x * 0.5 for x in range(0, 7)] 

# Kombinasyonları oluştur
refund_scenarios = []
for c_type in class_types:
    for day in days_to_test:
        refund_scenarios.append((c_type, day))

@pytest.mark.parametrize("class_type, days_before", refund_scenarios)
def test_refund_scale(class_type, days_before):
    paid_amount = 100.0
    
    # --- 1. Beklenen İade Oranını Belirle (README Kuralları) ---
    expected_rate = 0.0
    
    # KURAL: 2 gün (dahil) ve öncesi ise %100
    if days_before >= 2.0:
        expected_rate = 1.0 # %100
        
    # KURAL: 2 günden az kaldıysa derse özel kesinti oranları
    else:
        if class_type == "Yoga": expected_rate = 0.30       # %30 alır
        elif class_type == "Boxing": expected_rate = 0.50   # %50 alır
        elif class_type == "Fitness": expected_rate = 0.10  # %10 alır
        elif class_type == "Basketball": expected_rate = 0.40 # %40 alır
        elif class_type == "Tennis": expected_rate = 0.80   # %80 alır
        elif class_type == "Swimming": expected_rate = 0.15 # %15 alır

    expected_refund = paid_amount * expected_rate

    # --- 2. Fonksiyonu Çalıştır ---
    actual_refund = calculate_refund(class_type, paid_amount, days_before)
    
    # --- 3. Karşılaştır ---
    # Float karşılaştırması için approx kullanıyoruz
    assert actual_refund == pytest.approx(expected_refund), \
        f"HATA: {class_type} için {days_before} gün kala: Beklenen {expected_refund}, Gelen {actual_refund}"