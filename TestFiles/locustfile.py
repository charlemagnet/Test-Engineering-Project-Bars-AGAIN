from locust import HttpUser, task, between
import random

class GymUser(HttpUser):
    # Kullanıcılar işlemler arasında 1-3 saniye beklesin
    wait_time = between(1, 3)
    
    activities = ["Yoga", "Boxing", "Fitness", "Tennis", "Basketball", "Swimming"]
    membership_types = ["Standard", "Student", "Premium"]

    def on_start(self):
        """
        HER KULLANICI BAŞLADIĞINDA YENİ BİR ÜYE OLARAK KAYDOLUR.
        Eskiden SQLite burada patlıyordu, şimdi PostgreSQL bunu rahatça kaldıracak.
        """
        self.name = f"Locust_User_{random.randint(1, 1000000)}"
        self.password = "pass123"
        self.membership_type = random.choice(self.membership_types)
        
        # /register endpoint'ine POST isteği (Veritabanına YAZMA işlemi)
        response = self.client.post("/register", json={
            "name": self.name,
            "password": self.password,
            "membership_type": self.membership_type
        })
        
        if response.status_code == 200:
            self.member_id = response.json()["member_id"]
        else:
            self.member_id = None

    @task(3)
    def check_prices(self):
        if not self.member_id: return
        
        # Fiyat sorma (OKUMA işlemi)
        activity = random.choice(self.activities)
        hour = random.randint(6, 23)
        self.client.get(
            f"/price?activity={activity}&hour={hour}&membership={self.membership_type}",
            name="/price (Check)"
        )

    @task(1)
    def make_reservation(self):
        if not self.member_id: return
        
        # Rezervasyon yapma (YAZMA işlemi)
        # Çakışma olmaması için her seferinde rastgele bir sınıf ismine rezervasyon yapıyoruz
        activity = random.choice(self.activities)
        class_name = f"{activity}_Group_{random.randint(1, 9999)}"
        
        self.client.post("/reservations", json={
            "user_id": self.member_id,
            "class_name": class_name,
            "class_type": activity,
            "hour": random.randint(8, 20)
        }, name="/reservations (Book)")

    @task(1)
    def view_my_reservations(self):
        if not self.member_id: return
        self.client.get(f"/my_reservations/{self.member_id}", name="/my_reservations")