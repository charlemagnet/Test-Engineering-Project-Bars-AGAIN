def get_base_price(class_type):
    prices = {
        "Yoga": 200,
        "Boxing": 120,
        "Fitness": 80,
        "Basketball": 40,
        "Tennis": 90,
        "Swimming": 30
    }
    # Geçersiz dersler için varsayılan bir değer veya hata yönetimi
    return prices.get(class_type, 100)

def calculate_dynamic_price(class_type, hour, membership_type="Standard"):
    base_price = get_base_price(class_type)
    
    # Zaman Çarpanı
    time_multiplier = 1.0
    if 6 <= hour < 12:  # Sabah İndirimi
        time_multiplier = 0.8
    elif 17 <= hour < 24: # Akşam Zammı
        time_multiplier = 1.1
    
    # Üyelik Çarpanı (Gelecekte genişletilebilir)
    member_multiplier = 1.0
    if membership_type == "Student":
        member_multiplier = 0.9  # Örnek: Öğrenciye ekstra indirim
    
    final_price = base_price * time_multiplier * member_multiplier
    return round(final_price, 2)