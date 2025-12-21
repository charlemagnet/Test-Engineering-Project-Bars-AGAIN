import psycopg2
from psycopg2.extras import RealDictCursor # <-- BU EKLENDİ
import os
import time

class DatabaseManager:
    def __init__(self, db_name="gym_db"):
        # Docker ortamından bilgileri al, yoksa varsayılanları kullan
        self.host = os.getenv("DB_HOST", "localhost")
        self.database = os.getenv("DB_NAME", "gym_db")
        self.user = os.getenv("DB_USER", "admin")
        self.password = os.getenv("DB_PASSWORD", "password123")
        self.connection = None
        self.connect()

    def connect(self):
        """Veritabanına bağlanır, başarısız olursa tekrar dener (Retry Logic)"""
        while True:
            try:
                self.connection = psycopg2.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password,
                    cursor_factory=RealDictCursor  # <-- ÖNEMLİ: Verileri Sözlük (Dict) olarak döndürür
                )
                self.connection.autocommit = True
                print("✅ PostgreSQL bağlantısı başarılı!")
                self.create_tables() # Bağlanınca tabloları kontrol et
                break
            except Exception as e:
                print(f"⏳ Veritabanına bağlanılamadı, 2 saniye içinde tekrar denenecek... Hata: {e}")
                time.sleep(2)

    def create_tables(self):
        """Tabloları oluşturur"""
        # cursor_factory zaten connect'te tanımlı olduğu için burada tekrar belirtmeye gerek yok
        with self.connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS members (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100),
                    membership_type VARCHAR(50),
                    password VARCHAR(100)
                );
            """)
            print("✅ Tablolar hazır.")

    def add_member(self, member_id, name, membership_type, password):
        """Yeni üye ekler"""
        with self.connection.cursor() as cursor:
            # Önce var mı diye kontrol et
            cursor.execute("SELECT id FROM members WHERE id = %s;", (member_id,))
            if cursor.fetchone():
                 raise ValueError(f"Member with ID {member_id} already exists.")

            # Yoksa ekle
            cursor.execute("""
                INSERT INTO members (id, name, membership_type, password)
                VALUES (%s, %s, %s, %s);
            """, (member_id, name, membership_type, password))

    def get_member(self, member_id):
        """ID ile üye getirir (Dict döner)"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM members WHERE id = %s;", (member_id,))
            return cursor.fetchone() # Artık {id: 1, name: '...'} formatında döner

    def delete_member(self, member_id):
        """Üyeyi siler (Testler ve temizlik için gerekli)"""
        with self.connection.cursor() as cursor:
            cursor.execute("DELETE FROM members WHERE id = %s;", (member_id,))
            return True # Silme işlemi başarılı kabul edilir

    def authenticate(self, member_id, password):
        """Giriş kontrolü"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM members WHERE id = %s AND password = %s;", (member_id, password))
            return cursor.fetchone()

    def get_all_members(self):
        """Tüm üyeleri listeler"""
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT * FROM members;")
            return cursor.fetchall()
            
    def close(self):
        """Bağlantıyı kapatır"""
        if self.connection:
            self.connection.close()