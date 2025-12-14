def calculate_refund(class_type, paid_amount, days_before):
    # Geçersiz ders kontrolü
    valid_classes = ["Yoga", "Boxing", "Fitness", "Basketball", "Tennis", "Swimming"]
    if class_type not in valid_classes:
        raise KeyError("Invalid class type")
        
    if paid_amount == 0:
        return 0.0
        
    # Kural 1: 2 gün (48 saat) veya daha önce iptal edilirse %100 iade
    if days_before >= 2.0:
        return float(paid_amount)
    
    # Kural 2: 2 günden az kaldıysa derse özel kesinti oranları
    late_refund_rates = {
        "Yoga": 0.30,      # %30 iade
        "Boxing": 0.50,    # %50 iade
        "Fitness": 0.10,   # %10 iade
        "Basketball": 0.40,# %40 iade
        "Tennis": 0.80,    # %80 iade
        "Swimming": 0.15   # %15 iade
    }
    
    rate = late_refund_rates.get(class_type, 0.0)
    return float(paid_amount * rate)