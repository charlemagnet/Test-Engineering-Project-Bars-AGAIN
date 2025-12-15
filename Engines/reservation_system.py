class GymClass:
    def __init__(self, name, type, capacity):
        self.name = name
        self.type = type
        self.capacity = capacity
        self.booked_users = []

class ReservationSystem:
    def __init__(self):
        self.reservations = {} # Rezervasyonları burada saklayacağız {id: data}
        self.res_counter = 1   # Rezervasyon ID sayacı

    def book_class(self, user_id, gym_class, paid_price):
        if len(gym_class.booked_users) < gym_class.capacity:
            # Kullanıcıyı derse ekle
            gym_class.booked_users.append(user_id)
            
            # Rezervasyonu hafızaya (Sözlüğe) kaydet
            res_id = self.res_counter
            self.reservations[res_id] = {
                "id": res_id,
                "user_id": user_id,
                "class_name": gym_class.name,
                "class_type": gym_class.type,
                "paid_price": paid_price
            }
            self.res_counter += 1
            
            return {
                "status": "Confirmed", 
                "message": f"Reservation confirmed for {gym_class.name}",
                "reservation_id": res_id
            }
        else:
            raise ValueError("Class is full")

    def get_user_reservations(self, user_id):
        # Kullanıcının ID'sine ait tüm rezervasyonları bul ve liste olarak döndür
        found_reservations = []
        for res in self.reservations.values():
            if res["user_id"] == user_id:
                found_reservations.append(res)
        return found_reservations

    def cancel_reservation(self, res_id):
        # Rezervasyonu sil
        if res_id in self.reservations:
            del self.reservations[res_id]
            return True
        return False