# Python 3.10 slim sürümünü baz alıyoruz
FROM python:3.10-slim

# Çalışma dizinini ayarla
WORKDIR /app

# --- DEĞİŞİKLİK BURADA ---
# "apt-get install gcc..." satırını SİLDİK veya YORUM SATIRI yaptık.
# psycopg2-binary kullandığımız için derleyiciye (gcc) ihtiyacımız yok.
# Sadece çok nadir durumlarda libpq gerekebilir, gerekirse ekleriz ama şu an hız lazım.
# RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/* # Bağımlılıkları kopyala ve yükle
COPY requirements.txt .
# --no-cache-dir ile temiz kurulum yapıyoruz
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . .

# Uygulamayı başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]