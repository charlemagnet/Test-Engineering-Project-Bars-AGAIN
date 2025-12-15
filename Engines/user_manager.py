class Member:
    def __init__(self, id, name, membership_type, password):
        self.id = id
        self.name = name
        self.membership_type = membership_type
        self.password = password  # Yeni alan: Şifre
        self.is_active = True

class MemberRepository:
    def __init__(self):
        self.members = {}

    def add_member(self, member):
        self.members[member.id] = member

    def get_member(self, member_id):
        return self.members.get(member_id)
    
    # Giriş kontrolü için yeni fonksiyon
    def authenticate(self, member_id, password):
        member = self.get_member(member_id)
        if member and member.password == password:
            return member
        return None