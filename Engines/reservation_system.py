class GymClass:
    def __init__(self, name, type, capacity):
        self.name = name
        self.type = type
        self.capacity = capacity
        self.booked_users = []

class ReservationSystem:
    def __init__(self):
        self.reservations = {} # Hold the reservations
        self.res_counter = 1  # Reservation ID counter

    def book_class(self, user_id, gym_class, paid_price):
        # --- [FORMAL VERIFICATION BRIDGE START] ---
        
        # 1. PRECONDITION (Ön Koşul):
        # Check capacity before booking
        assert len(gym_class.booked_users) < gym_class.capacity, \
            f"Precondition Failed: Class {gym_class.name} is full! Capacity: {gym_class.capacity}"

        # for postcondition check
        old_user_count = len(gym_class.booked_users)
        
        # --- [ACTION] ---
        
        # book the user into the class
        gym_class.booked_users.append(user_id)
        
        res_id = self.res_counter
        self.reservations[res_id] = {
            "id": res_id,
            "user_id": user_id,
            "class_name": gym_class.name,
            "class_type": gym_class.type,
            "paid_price": paid_price
        }
        self.res_counter += 1
        
        # --- [FORMAL VERIFICATION BRIDGE CONTINUES] ---

        # 2. POSTCONDITION :
        # Check that the user count has increased by 1
        new_user_count = len(gym_class.booked_users)
        assert new_user_count == old_user_count + 1, \
            f"Postcondition Failed: User count did not increase by 1. Old: {old_user_count}, New: {new_user_count}"

        # 3. INVARIANT (Değişmez Kural):
        # Fix point for capacity invariant
        assert len(gym_class.booked_users) <= gym_class.capacity, \
            f"Invariant Failed: Capacity exceeded! Count: {new_user_count}, Cap: {gym_class.capacity}"

        return {
            "status": "Confirmed", 
            "message": f"Reservation confirmed for {gym_class.name}",
            "reservation_id": res_id
        }

    def get_user_reservations(self, user_id):
        found_reservations = []
        for res in self.reservations.values():
            if res["user_id"] == user_id:
                found_reservations.append(res)
        return found_reservations

    def cancel_reservation(self, res_id):
        if res_id in self.reservations:
            res_data = self.reservations[res_id]
            user_id = res_data["user_id"]
            class_name = res_data["class_name"]

            del self.reservations[res_id]
            return True
        return False