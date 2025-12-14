class GymClass:
    def __init__(self, name, type, capacity):
        self.name = name
        self.type = type
        self.capacity = capacity
        self.reserved_users = []
    
    @property
    def current_occupancy(self):
        return len(self.reserved_users)

class ReservationSystem:
    def book_class(self, user_id, gym_class):
        if user_id in gym_class.reserved_users:
            raise ValueError("Already booked")
            
        if gym_class.current_occupancy >= gym_class.capacity:
            raise ValueError("Class is full")
            
        gym_class.reserved_users.append(user_id)
        return {"status": "confirmed", "user_id": user_id, "class": gym_class.name}

    def cancel_booking(self, user_id, gym_class):
        if user_id in gym_class.reserved_users:
            gym_class.reserved_users.remove(user_id)
            return {"status": "cancelled"}
        return {"status": "not_found"}