def get_base_price(class_type):
    prices = {
        "Yoga": 200.0,
        "Boxing": 120.0,
        "Fitness": 80.0,
        "Basketball": 40.0,
        "Tennis": 90.0,
        "Swimming": 30.0
    }
    
    # DİKKAT: Eğer class_type listede yoksa Python otomatik olarak KeyError fırlatır.
    # Bu, testlerin beklediği "Hata Fırlatma" davranışıdır.
    if class_type not in prices:
        raise KeyError(f"Geçersiz Ders Tipi: {class_type}")
        
    return prices[class_type]

def calculate_dynamic_price(class_type, hour, member_type):
    # get_base_price artık hata fırlatabileceği için burası da güvenli hale geldi
    base_price = get_base_price(class_type)
    
    time_multiplier = 1.0
    if 6 <= hour < 12:
        time_multiplier = 0.8
    elif 17 <= hour < 24:
        time_multiplier = 1.1
        
    member_multiplier = 1.0
    if member_type == "Student":
        member_multiplier = 0.8
    elif member_type == "Premium":
        member_multiplier = 1.4

    final_price = base_price * time_multiplier * member_multiplier
    return round(final_price, 2)