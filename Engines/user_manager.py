from Engines.database_manager import DatabaseManager

class Member:
    def __init__(self, id, name, membership_type, password):
        self.id = id
        self.name = name
        self.membership_type = membership_type
        self.password = password

class MemberRepository:
    def __init__(self):
        # Artık Mock liste yerine gerçek veritabanını kullanıyoruz
        self.db = DatabaseManager()

    def add_member(self, member):
        """Veritabanına yeni üye ekler"""
        self.db.add_member(member.id, member.name, member.membership_type, member.password)

    def get_member(self, member_id):
        """Veritabanından üye çeker ve Member objesine çevirir"""
        row = self.db.get_member(member_id)
        if row:
            # DÜZELTME: Artık row bir sözlük {"id": 1, "name": ...}
            return Member(row["id"], row["name"], row["membership_type"], row["password"])
        return None

    def authenticate(self, member_id, password):
        """Şifre kontrolü yapar"""
        row = self.db.authenticate(member_id, password)
        if row:
            # DÜZELTME: Index yerine Key kullanıyoruz
            return Member(row["id"], row["name"], row["membership_type"], row["password"])
        return None

    def delete_member(self, member_id):
        """Üyeyi siler"""
        return self.db.delete_member(member_id)

    def get_all_users_for_admin(self):
        """Admin paneli için tüm üyeleri listeler"""
        rows = self.db.get_all_members()
        users = []
        for row in rows:
            # DÜZELTME BURADA: row[0] yerine row["id"] vb.
            users.append({
                "id": row["id"],
                "name": row["name"],
                "type": row["membership_type"], # DB'de sütun adı 'membership_type'
                "password": row["password"]
            })
        return users