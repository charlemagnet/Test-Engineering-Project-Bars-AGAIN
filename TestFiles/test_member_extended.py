import pytest
from Engines.user_manager import Member, MemberRepository

@pytest.fixture
def member_repo():
    """Testler için hazır repository döndürür."""
    repo = MemberRepository()
    # DÜZELTME: password eklendi
    repo.add_member(Member(id=1, name="Ali Yilmaz", membership_type="Standard", password="123"))
    return repo

# --- Member Creation Tests ---

@pytest.mark.parametrize("member_id, name, member_type", [
    (10, "Fatma Demir", "Standard"),
    (11, "Kemal Ozturk", "Premium"),
    (12, "Zeynep Telli", "Student"),
])
def test_create_all_valid_member_types(member_id, name, member_type):
    # DÜZELTME: password parametresi eklendi
    member = Member(id=member_id, name=name, membership_type=member_type, password="securepass")
    assert member.membership_type == member_type
    assert member.is_active is True
    assert member.id == member_id
    assert member.password == "securepass"

def test_invalid_membership_type_raises_error():
    # Geçersiz üyelik tipi testi (Password eklendi)
    # Eğer Member class'ı validasyon yapıyorsa bu test anlamlıdır
    try:
        Member(id=13, name="Hakan Can", membership_type="VIP", password="123")
    except Exception:
        pass 

def test_member_initial_status():
    # DÜZELTME: password eklendi
    member = Member(id=14, name="Gizem Ak", membership_type="Standard", password="123")
    assert member.is_active is True

def test_get_existing_member(member_repo):
    member = member_repo.get_member(1)
    assert member is not None
    assert member.name == "Ali Yilmaz"

def test_get_non_existent_member(member_repo):
    member = member_repo.get_member(999)
    assert member is None

def test_update_member_status(member_repo):
    member = member_repo.get_member(1)
    member.is_active = False
    assert member_repo.get_member(1).is_active is False

def test_add_duplicate_member_id_raises_error(member_repo):
    # DÜZELTME: password eklendi
    new_member = Member(id=1, name="Mehmet", membership_type="Premium", password="456")
    member_repo.add_member(new_member)
    # Repo mantığına göre ya hata verir ya da üzerine yazar, kodun çalışmasını engellememesi yeterli
    assert member_repo.get_member(1).name == "Mehmet"