import pytest
# Assuming user_manager contains the Member class and repository logic
# from user_manager import Member, MemberRepository 

@pytest.fixture
def member_repo():
    """Fixture to provide a fresh repository instance for each test."""
    repo = MemberRepository()
    repo.add_member(Member(id=1, name="Ali Yilmaz", membership_type="Standard"))
    return repo

# --- Member Creation Tests ---

@pytest.mark.parametrize("member_id, name, member_type", [
    (10, "Fatma Demir", "Standard"),
    (11, "Kemal Ozturk", "Premium"),
    (12, "Zeynep Telli", "Student"),
])
def test_create_all_valid_member_types(member_id, name, member_type):
    """Tests the successful creation of all defined membership types (Standard, Premium, Student)."""
    member = Member(id=member_id, name=name, membership_type=member_type)
    assert member.membership_type == member_type
    assert member.is_active is True
    assert member.id == member_id

def test_invalid_membership_type_raises_error():
    """Ensures a ValueError is raised when an invalid membership type is passed."""
    with pytest.raises(ValueError, match="Invalid membership type"):
        Member(id=13, name="Hakan Can", membership_type="VIP")

def test_member_initial_status():
    """Verifies that a newly created member is set to active by default."""
    member = Member(id=14, name="Gizem Ak", membership_type="Standard")
    assert member.is_active is True

# --- Member Repository Tests ---

def test_get_existing_member(member_repo):
    """Tests retrieving a member that exists in the repository."""
    member = member_repo.get_member_by_id(1)
    assert member is not None
    assert member.name == "Ali Yilmaz"
    assert member.membership_type == "Standard"

def test_get_non_existent_member(member_repo):
    """Tests that retrieving a non-existent member returns None or raises an appropriate exception."""
    member = member_repo.get_member_by_id(999)
    assert member is None # Assuming the repository returns None

def test_update_member_status(member_repo):
    """Tests the ability to deactivate a member."""
    member_repo.deactivate_member(1)
    updated_member = member_repo.get_member_by_id(1)
    assert updated_member.is_active is False

def test_add_duplicate_member_id_raises_error(member_repo):
    """Tests if adding a member with an existing ID is prevented."""
    with pytest.raises(ValueError, match="Member ID already exists"):
        member_repo.add_member(Member(id=1, name="Duplicate User", membership_type="Premium"))