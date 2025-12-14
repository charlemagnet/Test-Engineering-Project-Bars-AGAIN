import sqlite3

class DatabaseManager:
    def __init__(self, db_name="gym_system.db"):
        """
        Veritabanı bağlantısını başlatır.
        db_name: Veritabanı dosyasının adı. Testler için ':memory:' kullanılır.
        """
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()

    def create_tables(self):
        """Üyeler tablosunu oluşturur."""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS members (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                membership_type TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def add_member(self, member_id, name, membership_type):
        """Yeni bir üye ekler."""
        try:
            self.cursor.execute(
                "INSERT INTO members (id, name, membership_type) VALUES (?, ?, ?)", 
                (member_id, name, membership_type)
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            raise ValueError(f"Member with ID {member_id} already exists.")

    def get_member(self, member_id):
        """ID'ye göre üyeyi getirir. Bulamazsa None döner."""
        self.cursor.execute("SELECT * FROM members WHERE id=?", (member_id,))
        return self.cursor.fetchone()

    def delete_member(self, member_id):
        """ID'ye göre üyeyi siler."""
        self.cursor.execute("DELETE FROM members WHERE id=?", (member_id,))
        self.connection.commit()

    def close(self):
        """Bağlantıyı kapatır."""
        self.connection.close()