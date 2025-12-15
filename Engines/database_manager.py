import pytest
from Engines.database_manager import DatabaseManager 

@pytest.fixture
def db():
    manager = DatabaseManager(":memory:") 
    manager.create_tables() 
    return manager

def test_database_connection(db):
    assert db.connection is not None

def test_add_and_get_member(db):
    member_id = 101
    name = "Test User"
    m_type = "Premium"
    password = "123" # EKLENDİ
    
    # Şifre parametresi eklendi
    db.add_member(member_id, name, m_type, password)
    
    fetched_member = db.get_member(member_id)
    
    assert fetched_member is not None
    assert fetched_member[0] == member_id
    assert fetched_member[1] == name
    assert fetched_member[2] == m_type
    assert fetched_member[3] == password # EKLENDİ

def test_get_non_existent_member(db):
    result = db.get_member(9999)
    assert result is None

def test_delete_member(db):
    # Şifre parametresi eklendi
    db.add_member(202, "Silinecek User", "Standard", "pass123")
    
    assert db.get_member(202) is not None
    db.delete_member(202)
    assert db.get_member(202) is None