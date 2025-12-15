import pytest
from Engines.user_manager import Member, MemberRepository

@pytest.fixture
def member_repo():
    """
    Testler için geçici (RAM) veritabanı kullanan repository.
    Diskteki 'gym_system.db' dosyasını etkilemez.
    """
    # EKLENDİ: db_name=":memory:"
    repo = MemberRepository(db_name=":memory:")
    
    # Password eklendi
    repo.add_member(Member(id=1, name="Ali Yilmaz", membership_type="Standard", password="123"))
    return repo

def test_create_all_valid_member_types():
    # Password eklendi
    member = Member(id=10, name="Fatma", membership_type="Standard", password="pass")
    assert member.membership_type == "Standard"

def test_get_existing_member(member_repo):
    member = member_repo.get_member(1)
    assert member is not None
    assert member.name == "Ali Yilmaz"

def test_add_duplicate_member_id_raises_error(member_repo):
    # Password eklendi
    new_member = Member(id=1, name="Mehmet", membership_type="Premium", password="456")
    
    # Veritabanı unique constraint hatası fırlatır (ValueError olarak yakalanıyor mu kontrol etmeliyiz)
    with pytest.raises(ValueError):
        member_repo.add_member(new_member)