import pytest
from Engines.user_manager import MemberRepository, Member

# --- TEST KURULUMU (FIXTURE) ---
@pytest.fixture
def member_repo():
    """
    Testler için repository oluşturur.
    Her testten önce veritabanını temizler (Truncate) ki çakışma olmasın.
    """
    repo = MemberRepository() # Artık parametre almıyor!
    
    # Veritabanını Temizle (Clean Slate)
    with repo.db.connection.cursor() as cursor:
        cursor.execute("TRUNCATE TABLE members CASCADE;")
        # repo.db.connection.commit() # Autocommit açık olduğu için gerek yok ama zararı da yok
    
    return repo

# --- TESTLER ---

def test_add_duplicate_member_id_raises_error(member_repo):
    # 1. Üye ekle
    m1 = Member(101, "Original", "Standard", "pass1")
    member_repo.add_member(m1)
    
    # 2. Aynı ID ile tekrar eklemeye çalış
    m2 = Member(101, "Duplicate", "Premium", "pass2")
    
    # 3. Hata vermeli
    with pytest.raises(ValueError, match="already exists"):
        member_repo.add_member(m2)

def test_password_is_stored_correctly(member_repo):
    member = Member(202, "Secure User", "Premium", "secret_pass")
    member_repo.add_member(member)
    
    # Veritabanından geri çek
    retrieved = member_repo.get_member(202)
    
    # Şifre doğru mu?
    assert retrieved.password == "secret_pass"

def test_authenticate_success(member_repo):
    member = Member(303, "Auth User", "Standard", "my_password")
    member_repo.add_member(member)
    
    # Doğru şifreyle giriş
    result = member_repo.authenticate(303, "my_password")
    assert result is not None
    assert result.name == "Auth User"

def test_authenticate_failure(member_repo):
    member = Member(404, "Hacker Target", "Standard", "strong_pass")
    member_repo.add_member(member)
    
    # Yanlış şifreyle giriş
    result = member_repo.authenticate(404, "wrong_pass")
    assert result is None