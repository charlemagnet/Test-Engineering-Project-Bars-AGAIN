class Member:
    def __init__(self, id, name, membership_type):
        valid_types = ["Standard", "Premium", "Student"]
        if membership_type not in valid_types:
            raise ValueError("Invalid membership type")
            
        self.id = id
        self.name = name
        self.membership_type = membership_type
        self.is_active = True

class MemberRepository:
    def __init__(self):
        self.members = {}

    def add_member(self, member):
        if member.id in self.members:
            raise ValueError("Member ID already exists")
        self.members[member.id] = member

    def get_member_by_id(self, member_id):
        return self.members.get(member_id)

    def deactivate_member(self, member_id):
        member = self.get_member_by_id(member_id)
        if member:
            member.is_active = False