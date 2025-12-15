import sqlite3

class DatabaseManager:
    def __init__(self, db_name="gym_system.db"):
        self.db_name = db_name
        self.connection = None
        self.connect() # Bağlantıyı aç

    def connect(self):
        self.connection = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        # Password sütunu eklendi
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                membership_type TEXT NOT NULL,
                password TEXT NOT NULL 
            )
        """)
        self.connection.commit()

    def add_member(self, member_id, name, membership_type, password):
        try:
            self.cursor.execute(
                "INSERT INTO members (id, name, membership_type, password) VALUES (?, ?, ?, ?)", 
                (member_id, name, membership_type, password)
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"Member with ID {member_id} already exists.")

    def get_member(self, member_id):
        self.cursor.execute("SELECT * FROM members WHERE id=?", (member_id,))
        return self.cursor.fetchone()
    
    def get_all_members(self):
        # Arayüzde listelemek için tüm üyeleri çeken fonksiyon
        self.cursor.execute("SELECT * FROM members")
        return self.cursor.fetchall()

    def delete_member(self, member_id):
        self.cursor.execute("DELETE FROM members WHERE id=?", (member_id,))
        self.connection.commit()