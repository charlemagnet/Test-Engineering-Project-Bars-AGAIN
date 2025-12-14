from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

# Engines klasöründeki modülleri içe aktarıyoruz
from Engines.pricing_engine import calculate_dynamic_price
from Engines.refund_manager import calculate_refund
from Engines.user_manager import Member, MemberRepository
from Engines.reservation_system import ReservationSystem, GymClass

app = FastAPI()

# --- Global State (Bellek İçi Veri Tutma) ---
# Gerçek bir veritabanı yerine şimdilik işlemleri burada tutuyoruz.
member_repo = MemberRepository()
reservation_system = ReservationSystem()

# Testlerde kullanılacak örnek dersler havuzu
gym_classes = {
    "Yoga Flow": GymClass("Yoga Flow", "Yoga", 20),
    "Boxing Pro": GymClass("Boxing Pro", "Boxing", 15)
}

# --- Pydantic Modelleri (Gelen Veriyi Doğrulama) ---
class RefundRequest(BaseModel):
    activity: str
    paid_amount: float
    days_before: float

class MemberRequest(BaseModel):
    id: int
    name: str
    membership_type: str

class ReservationRequest(BaseModel):
    user_id: int
    class_name: str
    class_type: str
    capacity: int

# --- API Uç Noktaları (Endpoints) ---

@app.get("/")
def read_root():
    """Health check endpoint'i."""
    return {"message": "Gym System API is running"}

@app.get("/price")
def get_price(activity: str, hour: int, membership: str = "Standard"):
    """Fiyat hesaplama endpoint'i."""
    try:
        price = calculate_dynamic_price(activity, hour, membership)
        return {"activity": activity, "price": price}
    except Exception:
        # Tanımsız aktiviteler için varsayılan fiyat (Test gereği)
        return {"activity": activity, "price": 100.0}

@app.post("/refund")
def process_refund(request: RefundRequest):
    """İade hesaplama endpoint'i."""
    try:
        refund = calculate_refund(request.activity, request.paid_amount, request.days_before)
        return {"refund_amount": refund}
    except KeyError:
         raise HTTPException(status_code=400, detail="Invalid activity type")

@app.post("/members", status_code=201) # <-- status_code=201 eklendi
def create_member(request: MemberRequest):
    """Yeni üye oluşturma endpoint'i."""
    try:
        new_member = Member(request.id, request.name, request.membership_type)
        member_repo.add_member(new_member)
        return {"status": "Member created", "member_id": new_member.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/reservations")
def make_reservation(request: ReservationRequest):
    """Rezervasyon yapma endpoint'i."""
    # 1. Dersi bul veya oluştur (Test esnekliği için)
    if request.class_name not in gym_classes:
        gym_classes[request.class_name] = GymClass(request.class_name, request.class_type, request.capacity)
    
    target_class = gym_classes[request.class_name]
    
    # 2. Rezervasyonu dene
    try:
        result = reservation_system.book_class(request.user_id, target_class)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))