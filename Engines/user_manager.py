from Engines.database_manager import DatabaseManager

class Member:
    def __init__(self, id, name, membership_type, password):
        self.id = id
        self.name = name
        self.membership_type = membership_type
        self.password = password
        self.is_active = True

class MemberRepository:
    # EKLENDİ: db_name parametresi varsayılan olarak "gym_system.db"
    # Ama testlerde ":memory:" gönderebileceğiz.
    def __init__(self, db_name="gym_system.db"):
        self.db = DatabaseManager(db_name)
        self.db.create_tables()

    def add_member(self, member):
        self.db.add_member(member.id, member.name, member.membership_type, member.password)

    def get_member(self, member_id):
        row = self.db.get_member(member_id)
        if row:
            return Member(id=row[0], name=row[1], membership_type=row[2], password=row[3])
        return None
    
    def authenticate(self, member_id, password):
        member = self.get_member(member_id)
        if member and member.password == password:
            return member
        return None
        
    def get_all_users_for_admin(self):
        rows = self.db.get_all_members()
        users = []
        for row in rows:
             # Tuple: (id, name, type, password)
             users.append({"id": row[0], "name": row[1], "type": row[2], "password": row[3]})
        return users