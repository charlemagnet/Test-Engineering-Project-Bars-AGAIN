import pytest
from fastapi.testclient import TestClient

# Henüz main.py ve app nesnesi yok, bu yüzden burası hata verecek (RED Aşaması)
# TDD kuralı gereği: Önce testi yazıyoruz.
try:
    from main import app
    client = TestClient(app)
except ImportError:
    client = None

@pytest.fixture
def api_client():
    if client is None:
        pytest.fail("main.py dosyası veya 'app' nesnesi bulunamadı. Lütfen API'yi oluşturun.")
    return client

# --- 1. Health Check Test ---
def test_read_root(api_client):
    """API'nin ayakta olup olmadığını kontrol eder."""
    response = api_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Gym System API is running"}

# --- 2. Pricing API Tests ---
def test_get_price_yoga_morning(api_client):
    """
    GET /price endpoint'ini test eder.
    Senaryo: Yoga, Sabah 09:00, Standart üye.
    Beklenen: 200 * 0.8 = 160
    """
    response = api_client.get("/price?activity=Yoga&hour=9&membership=Standard")
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 160.0
    assert data["activity"] == "Yoga"

def test_get_price_invalid_activity(api_client):
    """Geçersiz aktivite girildiğinde varsayılan fiyatı veya hatayı kontrol eder."""
    response = api_client.get("/price?activity=Unknown&hour=14")
    # Mantığımıza göre varsayılan 100 dönüyordu
    assert response.status_code == 200 
    assert response.json()["price"] == 100.0

# --- 3. Refund API Tests ---
def test_calculate_refund_api(api_client):
    """
    POST /refund endpoint'ini test eder.
    Senaryo: Boxing, 1 gün kala (Geç iptal), 100 TL ödenmiş.
    Beklenen: Boxing kuralı %50 iade -> 50 TL
    """
    payload = {
        "activity": "Boxing",
        "paid_amount": 100.0,
        "days_before": 1.0
    }
    response = api_client.post("/refund", json=payload)
    assert response.status_code == 200
    assert response.json()["refund_amount"] == 50.0

# --- 4. Membership API Tests ---
def test_create_member_api(api_client):
    """
    POST /members endpoint'ini test eder.
    Yeni üye ekleme.
    """
    payload = {
        "id": 501,
        "name": "API Tester",
        "membership_type": "Premium"
    }
    response = api_client.post("/members", json=payload)
    assert response.status_code == 201  # Created
    assert response.json()["status"] == "Member created"
    assert response.json()["member_id"] == 501

# --- 5. Reservation API Tests ---
def test_make_reservation_api(api_client):
    """
    POST /reservations endpoint'ini test eder.
    """
    # Önce üye oluşturmamız gerekebilir veya mock kullanabiliriz.
    # Basitlik adına doğrudan rezervasyon isteği atıyoruz.
    payload = {
        "user_id": 501,
        "class_name": "Yoga Flow",
        "class_type": "Yoga",
        "capacity": 20
    }
    response = api_client.post("/reservations", json=payload)
    
    # Başarılı rezervasyon
    assert response.status_code == 200
    assert response.json()["status"] == "confirmed"