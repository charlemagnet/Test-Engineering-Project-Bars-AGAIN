VALID_CLASSES = ["Yoga", "Boxing", "Fitness", "Basketball", "Tennis", "Swimming"]

def calculate_refund(class_type, paid_amount, days_before):
    # 1. Geçersiz Ders Kontrolü (Strict Validation)
    if class_type not in VALID_CLASSES:
        raise KeyError(f"Geçersiz Ders Tipi: {class_type}")

    # 2. "Before two enterance" -> %100 İade
    # (2 gün ve daha öncesinde iptal ederse paranın tamamını alır)
    if days_before >= 2.0:
        return float(paid_amount)
    
    # 3. "After that" -> Ders tipine özel ceza oranları
    # (2 günden az kalmışsa, README'deki oranları uygula)
    late_refund_rates = {
        "Yoga": 0.30,       # %30 alır
        "Boxing": 0.50,     # %50 alır
        "Fitness": 0.10,    # %10 alır
        "Basketball": 0.40, # %40 alır
        "Tennis": 0.80,     # %80 alır (User prompt: "Tenis")
        "Swimming": 0.15    # %15 alır
    }
    
    # Oranı al ve hesapla
    rate = late_refund_rates[class_type]
    return float(paid_amount * rate)