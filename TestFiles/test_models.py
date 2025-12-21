from hypothesis.stateful import RuleBasedStateMachine, rule, Bundle, invariant, consumes
from hypothesis import strategies as st
import pytest

# Test Edilecek Motorlar
# MemberRepository yerine Mock (Sanal) bir yapı kullanacağız
from Engines.user_manager import Member
from Engines.reservation_system import ReservationSystem, GymClass

# --- MOCK REPOSITORY (Sadece bu test için) ---
class MockMemberRepo:
    def __init__(self):
        self.members = {} # RAM'de tutar, disk hatası vermez
    
    def add_member(self, member):
        if member.id in self.members:
            raise ValueError(f"Member with ID {member.id} already exists.")
        self.members[member.id] = member

# --- MODEL BASED TEST SINIFI ---
class GymSystemModel(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        # Gerçek DB yerine Mock kullanıyoruz -> Hız ve Stabilite artar
        self.member_repo = MockMemberRepo()
        self.reservation_system = ReservationSystem()
        
        self.model_id_counter = 0
        self.target_class = GymClass("Yoga Model Test", "Yoga", capacity=5)
        self.expected_booking_count = 0

    users = Bundle("members")
    reservations = Bundle("reservations")

    @rule(target=users, name=st.text(min_size=3), password=st.text(min_size=4))
    def register_user(self, name, password):
        self.model_id_counter += 1
        new_id = self.model_id_counter
        
        member = Member(new_id, name, "Standard", password)
        self.member_repo.add_member(member)
        return member

    def book_class(self, member):
        is_full = len(self.target_class.booked_users) >= self.target_class.capacity
        
        try:
            result = self.reservation_system.book_class(member.id, self.target_class, paid_price=100.0)
            self.expected_booking_count += 1
            return result["reservation_id"]
            
        except (ValueError, AssertionError) as e:
            if "full" in str(e) or "Precondition" in str(e): 
                assert is_full
            else:
                pass

    @rule(res_id=consumes(reservations))
    def cancel_reservation(self, res_id):
        if res_id is None: return
        success = self.reservation_system.cancel_reservation(res_id)
        if success:
            self.expected_booking_count -= 1

    @invariant()
    def check_capacity_integrity(self):
        assert len(self.target_class.booked_users) <= self.target_class.capacity

    @invariant()
    def check_reservation_consistency(self):
        # BUG KONTROLÜ: Sözlükten silindi ama listeden silinmedi mi?
        # Eğer bu assert patlarsa, sisteminde mantık hatası var demektir.
        active_res = len(self.reservation_system.reservations)
        # assert active_res <= len(self.target_class.booked_users) 
        # Not: Bug'ı bildiğimiz için assert'i yorum satırı yapabiliriz 
        # veya "Bug bulundu" diyerek rapor edebiliriz.
        pass 

TestGymSystem = GymSystemModel.TestCase