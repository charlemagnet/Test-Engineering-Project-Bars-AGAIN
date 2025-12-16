import sqlite3
import psycopg2
import os
import time
import threading  # <--- EKLENDİ: Kilitleme mekanizması için

class DatabaseManager:
    def __init__(self, db_name="gym_system.db"):
        self.db_type = os.getenv("DB_TYPE", "sqlite")
        self.lock = threading.Lock() # <--- EKLENDİ: Her işlem bu kilidi bekleyecek
        
        # Testler için memory zorlaması
        if db_name == ":memory:":
            self.db_type = "sqlite"

        if self.db_type == "postgres":
            # Retry Mekanizması
            max_retries = 10
            for i in range(max_retries):
                try:
                    self.connection = psycopg2.connect(
                        host=os.getenv("DB_HOST", "db"),
                        database=os.getenv("DB_NAME", "gym_db"),
                        user=os.getenv("DB_USER", "gym_user"),
                        password=os.getenv("DB_PASS", "gym_password")
                    )
                    # Postgres'te her sorguda commit gerekmemesi için autocommit açabiliriz
                    # Ama senin yapın manuel commit'e göre, o yüzden şimdilik kapalı kalsın.
                    print("✅ Veritabanına başarıyla bağlanıldı!")
                    break
                except psycopg2.OperationalError:
                    print(f"⏳ Veritabanı henüz hazır değil, bekleniyor... ({i+1}/{max_retries})")
                    time.sleep(3)
            else:
                raise Exception("❌ Veritabanına bağlanılamadı! Zaman aşımı.")
        else:
            self.connection = sqlite3.connect(db_name, check_same_thread=False)

        self.cursor = self.connection.cursor()
        self.create_tables()

    def _execute(self, query, params=None):
        if self.db_type == "postgres":
            query = query.replace("?", "%s")
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

    # --- TÜM METODLARA 'with self.lock:' EKLENDİ ---

    def create_tables(self):
        with self.lock: # Aynı anda sadece bir thread tablo oluşturabilir
            self._execute("""
                CREATE TABLE IF NOT EXISTS members (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    membership_type TEXT NOT NULL,
                    password TEXT NOT NULL 
                )
            """)
            self.connection.commit()

    def add_member(self, member_id, name, membership_type, password):
        with self.lock: # KİLİT! Çarpışmayı önler.
            try:
                self._execute(
                    "INSERT INTO members (id, name, membership_type, password) VALUES (?, ?, ?, ?)", 
                    (member_id, name, membership_type, password)
                )
                self.connection.commit()
            except (sqlite3.IntegrityError, psycopg2.errors.UniqueViolation):
                self.connection.rollback()
                # Zaten varsa hata fırlatmadan geçebiliriz veya yönetebiliriz
                # Stres testinde hata oranını düşürmek için 'pass' diyebilirsin
                # Ama doğrusu raise etmektir.
                raise ValueError(f"Member with ID {member_id} already exists.")
            except Exception as e:
                self.connection.rollback()
                raise e

    def get_member(self, member_id):
        with self.lock:
            self._execute("SELECT * FROM members WHERE id=?", (member_id,))
            return self.cursor.fetchone()
    
    def get_all_members(self):
        with self.lock:
            self._execute("SELECT * FROM members")
            return self.cursor.fetchall()

    def delete_member(self, member_id):
        with self.lock:
            self._execute("DELETE FROM members WHERE id=?", (member_id,))
            self.connection.commit()

    def close(self):
        self.connection.close()