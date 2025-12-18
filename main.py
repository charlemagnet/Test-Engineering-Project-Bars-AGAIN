import secrets
from fastapi import FastAPI, HTTPException, Header, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Engines importları
from Engines.pricing_engine import calculate_dynamic_price
from Engines.user_manager import Member, MemberRepository
from Engines.reservation_system import ReservationSystem, GymClass

app = FastAPI()

# --- GÜVENLİK YAMASI 1: Eksik Security Header'ları Ekleme ---
# OWASP ZAP'ın "Missing Security Headers" uyarısını çözer.
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"  # MIME-type sniffing engelleme
    response.headers["X-Frame-Options"] = "DENY"            # Clickjacking koruması
    return response

# CORS Ayarı
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State
member_repo = MemberRepository()
reservation_system = ReservationSystem()
gym_classes = {
    "Yoga Flow": GymClass("Yoga Flow", "Yoga", 20),
    "Boxing Pro": GymClass("Boxing Pro", "Boxing", 15)
}

# --- BUG FIX: ID Sayacı Düzeltmesi ---
# Sunucu her açıldığında veritabanındaki en son ID'yi bulur ve oradan devam eder.
# Böylece "Unique constraint failed" hatası asla yaşanmaz.
existing_users = member_repo.get_all_users_for_admin()
if existing_users:
    # Veritabanında üye varsa, en büyük ID'yi bul
    max_id = max(user["id"] for user in existing_users)
    current_id_counter = max_id
else:
    # Hiç üye yoksa 1000'den başla
    current_id_counter = 1000

# --- Güvenlik: Admin Basic Auth ---
security = HTTPBasic()

def get_current_admin(credentials: HTTPBasicCredentials = Depends(security)):
    # Kullanıcı adı ve şifre kontrolü (Güvenli karşılaştırma için secrets kullanılır)
    correct_username = secrets.compare_digest(credentials.username, "admin")
    correct_password = secrets.compare_digest(credentials.password, "admin01")
    
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Hatalı Kullanıcı Adı veya Şifre",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# --- Pydantic Modelleri ---
class RegisterRequest(BaseModel):
    name: str
    password: str
    membership_type: str

class LoginRequest(BaseModel):
    member_id: int
    password: str

class ReservationRequest(BaseModel):
    user_id: int
    class_name: str
    class_type: str
    hour: int 

class CancellationRequest(BaseModel):
    reservation_id: int
    entrances_used: int

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Gym System API is running"}

@app.post("/register")
def register_member(request: RegisterRequest):
    global current_id_counter
    current_id_counter += 1  # Otomatik ID artır
    new_id = current_id_counter
    
    new_member = Member(new_id, request.name, request.membership_type, request.password)
    
    # Hata yakalama bloğu ile ekstra güvenlik
    try:
        member_repo.add_member(new_member)
    except ValueError as e:
        # Nadir de olsa çakışma olursa kullanıcıya düzgün hata dön
        raise HTTPException(status_code=400, detail=str(e))
    
    return {
        "status": "success", 
        "message": "Kayıt Başarılı!", 
        "member_id": new_id,
        "name": new_member.name,
        "membership_type": new_member.membership_type
    }

@app.post("/login")
def login_member(request: LoginRequest):
    user = member_repo.authenticate(request.member_id, request.password)
    if user:
        return {
            "status": "success", 
            "member_id": user.id, 
            "name": user.name, 
            "membership_type": user.membership_type
        }
    else:
        raise HTTPException(status_code=401, detail="Hatalı ID veya Şifre")

@app.get("/price")
def get_price(activity: str, hour: int, membership: str):
    try:
        # Fiyatı hesaplamaya çalış
        price = calculate_dynamic_price(activity, hour, membership)
        return {"price": price}
    except KeyError:
        raise HTTPException(status_code=400, detail="Gecersiz aktivite tipi")

# --- Rezervasyon Listeleme Endpoint'i ---
@app.get("/my_reservations/{user_id}")
def get_my_reservations(user_id: int):
    return reservation_system.get_user_reservations(user_id)
# -------------------------------------------------------

@app.post("/cancel_reservation")
def cancel_reservation(request: CancellationRequest):
    res_data = reservation_system.reservations.get(request.reservation_id)
    if not res_data:
        raise HTTPException(status_code=404, detail="Rezervasyon bulunamadı")

    class_type = res_data["class_type"]
    paid_amount = res_data["paid_price"]
    entrances = request.entrances_used

    refund_amount = 0.0
    
    if entrances < 2:
        refund_amount = float(paid_amount)
        message = "2 dersten az katılım olduğu için %100 iade yapıldı."
    else:
        rates = {
            "Yoga": 0.30,       
            "Boxing": 0.50,     
            "Fitness": 0.10,    
            "Basketball": 0.40, 
            "Tennis": 0.80,     
            "Swimming": 0.15    
        }
        rate = rates.get(class_type, 0.0)
        refund_amount = paid_amount * rate
        message = f"{entrances} ders işlendiği için kesintili iade ({class_type} oranı: %{rate*100})."

    reservation_system.cancel_reservation(request.reservation_id)

    return {
        "status": "Cancelled",
        "refund_amount": round(refund_amount, 2),
        "message": message
    }

@app.post("/reservations")
def make_reservation(request: ReservationRequest):
    if request.class_name not in gym_classes:
        gym_classes[request.class_name] = GymClass(request.class_name, request.class_type, 20)
    target_class = gym_classes[request.class_name]
    
    try:
        user = member_repo.get_member(request.user_id)
        price_to_pay = 100.0 
        if user:
            price_to_pay = calculate_dynamic_price(request.class_type, request.hour, user.membership_type)
            
        result = reservation_system.book_class(request.user_id, target_class, price_to_pay)
        result["price_to_pay"] = price_to_pay
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# --- ADMIN PANELI (GÜVENLİ) ---
@app.get("/admin/users")
def get_all_users(username: str = Depends(get_current_admin)):
    """
    Veritabanındaki tüm üyeleri listeler.
    Güvenlik: Basic Auth (Kullanıcı Adı: admin, Şifre: admin01) gerektirir.
    """
    return member_repo.get_all_users_for_admin()