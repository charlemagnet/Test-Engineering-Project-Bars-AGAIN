import pytest
import sqlite3
# Henüz bu dosya yok, import hatası alacağız (Bu beklenen bir durum)
# from database_manager import DatabaseManager 

@pytest.fixture
def db():
    """
    Her testten önce geçici (RAM üzerinde) bir veritabanı oluşturur.
    Test bitince bağlantı kapanır.
    """
    # :memory: parametresi diske yazmadan RAM'de çalışmasını sağlar
    manager = DatabaseManager(":memory:") 
    manager.create_tables() # Tabloları oluşturmasını bekliyoruz
    return manager

def test_database_connection(db):
    """Veritabanı bağlantısının başarılı olup olmadığını test eder."""
    assert db.connection is not None

def test_add_and_get_member(db):
    """
    Veritabanına bir üye ekleyip, SQL sorgusu ile geri alabilmeyi test eder.
    """
    # 1. Veri Ekleme
    member_id = 101
    name = "Test User"
    m_type = "Premium"
    
    db.add_member(member_id, name, m_type)
    
    # 2. Veri Okuma
    fetched_member = db.get_member(member_id)
    
    # 3. Doğrulama (Tuple döneceğini varsayıyoruz: (id, name, type))
    assert fetched_member is not None
    assert fetched_member[0] == member_id
    assert fetched_member[1] == name
    assert fetched_member[2] == m_type

def test_get_non_existent_member(db):
    """Olmayan bir üyeyi sorguladığımızda None dönmeli."""
    result = db.get_member(9999)
    assert result is None

def test_delete_member(db):
    """Üye silme işlemini test eder."""
    db.add_member(202, "Silinecek User", "Standard")
    
    # Önce var olduğunu teyit et
    assert db.get_member(202) is not None
    
    # Sil
    db.delete_member(202)
    
    # Artık yok olduğunu teyit et
    assert db.get_member(202) is None