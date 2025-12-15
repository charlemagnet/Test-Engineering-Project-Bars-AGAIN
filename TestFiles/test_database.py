import pytest
from Engines.database_manager import DatabaseManager 

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
    password = "test_password_123" # <--- YENİ: Şifre tanımladık
    
    # YENİ: add_member artık 4 parametre alıyor
    db.add_member(member_id, name, m_type, password)
    
    # 2. Veri Okuma
    fetched_member = db.get_member(member_id)
    
    # 3. Doğrulama (Tuple döneceğini varsayıyoruz: (id, name, type, password))
    assert fetched_member is not None
    assert fetched_member[0] == member_id
    assert fetched_member[1] == name
    assert fetched_member[2] == m_type
    # Veritabanından şifrenin de doğru gelip gelmediğini kontrol edelim
    assert fetched_member[3] == password 

def test_get_non_existent_member(db):
    """Olmayan bir üyeyi sorguladığımızda None dönmeli."""
    result = db.get_member(9999)
    assert result is None

def test_delete_member(db):
    """Üye silme işlemini test eder."""
    # YENİ: Buraya da rastgele bir şifre ("123456") ekledik
    db.add_member(202, "Silinecek User", "Standard", "123456")
    
    # Önce var olduğunu teyit et
    assert db.get_member(202) is not None
    
    # Sil
    db.delete_member(202)
    
    # Artık yok olduğunu teyit et
    assert db.get_member(202) is None