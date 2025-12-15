import pytest
from starlette.testclient import TestClient
from main import app, member_repo
from Engines.database_manager import DatabaseManager

# EKLENDİ: Her testten önce API'nin veritabanını sıfırla (RAM'e al)
@pytest.fixture(autouse=True)
def override_db():
    # Main.py'deki global repo'nun veritabanını test için belleğe alıyoruz
    member_repo.db = DatabaseManager(":memory:")
    member_repo.db.create_tables()

@pytest.fixture
def api_client():
    return TestClient(app)

def test_read_root(api_client):
    response = api_client.get("/")
    assert response.status_code == 200

def test_create_member_api(api_client):
    payload = {
        "name": "API Tester",
        "password": "secure123",
        "membership_type": "Premium"
    }
    response = api_client.post("/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    # ID kontrolünü esnek yapabiliriz veya sıfırlandığı için 1001 bekleyebiliriz
    assert "member_id" in data
