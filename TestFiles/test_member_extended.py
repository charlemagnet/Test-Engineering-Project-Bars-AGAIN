import pytest
from Engines.user_manager import Member, MemberRepository

# --- Fixture (Hazırlık) ---
@pytest.fixture
def member_repo():
    """
    Testler için repository oluşturur.
    PostgreSQL kalıcı olduğu için önce temizlik yapar.
    """
    repo = MemberRepository(db_name=":memory:") # İsim sembolik, config'den okur
    
    # TEMİZLİK: Önceki testten kalan veri varsa sil
    # repo.db üzerinden DatabaseManager'ın delete_member fonksiyonuna ulaşıyoruz
    repo.db.delete_member(1)
    
    # Şimdi taze ekle
    repo.add_member(Member(id=1, name="Ali Yilmaz", membership_type="Standard", password="123"))
    
    yield repo
    
    # TEARDOWN: Test bitince de temizle (Opsiyonel ama iyi olur)
    repo.db.delete_member(1)

# --- Testler ---

def test_add_duplicate_member_id_raises_error(member_repo):
    """Aynı ID ile kayıt olmaya çalışınca hata vermeli"""
    # Zaten fixture içinde ID=1 eklendi.
    # Tekrar eklemeye çalışınca hata bekliyoruz.
    new_member = Member(id=1, name="Veli", membership_type="Premium", password="456")
    
    with pytest.raises(ValueError) as excinfo:
        member_repo.add_member(new_member)
    
    assert "already exists" in str(excinfo.value)

def test_password_is_stored_correctly(member_repo):
    """Şifrenin doğru kaydedildiğini doğrula"""
    user = member_repo.get_member(1)
    assert user is not None
    assert user.password == "123"

def test_authenticate_success(member_repo):
    """Doğru şifre ile giriş"""
    user = member_repo.authenticate(1, "123")
    assert user is not None
    assert user.name == "Ali Yilmaz"

def test_authenticate_failure(member_repo):
    """Yanlış şifre ile giriş"""
    user = member_repo.authenticate(1, "YANLIS_SIFRE")
    assert user is None