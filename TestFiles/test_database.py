import pytest
from Engines.database_manager import DatabaseManager

@pytest.fixture
def db():
    # 1. Bağlantı Kur
    manager = DatabaseManager()
    
    # --- TEMİZLİK (Clean Slate) ---
    # Test başlamadan önce tabloları KESİN boşalt
    try:
        with manager.connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE members CASCADE;")
    except Exception as e:
        print(f"Tablo temizlenirken hata: {e}")
    
    yield manager
    
    # Test bitince bağlantıyı kapat
    manager.close()

def test_database_connection(db):
    assert db.connection is not None
    assert db.connection.closed == 0

def test_add_and_get_member(db):
    """
    Veritabanına bir üye ekleyip, geri alabilmeyi test eder.
    """
    # 1. Veri Ekleme
    member_id = 101
    name = "Test User"
    m_type = "Premium"
    password = "test_password_123"

    db.add_member(member_id, name, m_type, password)
    
    # 2. Veri Okuma
    member = db.get_member(member_id)
    
    # 3. Doğrulama
    assert member is not None
    assert member["name"] == name
    assert member["membership_type"] == m_type

def test_get_non_existent_member(db):
    member = db.get_member(9999)
    assert member is None

def test_delete_member(db):
    # Önce ekle
    db.add_member(202, "To Be Deleted", "Standard", "pass")
    
    # Sonra sil
    result = db.delete_member(202)
    assert result is True
    
    # Silindi mi kontrol et
    assert db.get_member(202) is None