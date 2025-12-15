import pandas as pd
import matplotlib.pyplot as plt

def generate_decision_table_image():
    # 1. KARAR TABLOSU VERİLERİNİ HAZIRLA
    # Kodundaki mantığa göre tüm senaryoları buraya döküyoruz.
    data = {
        "Kural ID": ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9"],
        "Koşul: Saat Aralığı": [
            "Sabah (06:00 - 11:59)", "Sabah (06:00 - 11:59)", "Sabah (06:00 - 11:59)",
            "Standart (Diğer Saatler)", "Standart (Diğer Saatler)", "Standart (Diğer Saatler)",
            "Akşam (17:00 - 23:59)", "Akşam (17:00 - 23:59)", "Akşam (17:00 - 23:59)"
        ],
        "Koşul: Üyelik Tipi": [
            "Standard", "Student", "Premium",
            "Standard", "Student", "Premium",
            "Standard", "Student", "Premium"
        ],
        "Eylem: Zaman Çarpanı": [0.8, 0.8, 0.8, 1.0, 1.0, 1.0, 1.1, 1.1, 1.1],
        "Eylem: Üyelik Çarpanı": [1.0, 0.8, 1.4, 1.0, 0.8, 1.4, 1.0, 0.8, 1.4]
    }

    # Pandas DataFrame oluştur
    df = pd.DataFrame(data)

    # Sonuç sütununu (Total Multiplier) otomatik hesapla
    df["SONUÇ (Toplam Çarpan)"] = df["Eylem: Zaman Çarpanı"] * df["Eylem: Üyelik Çarpanı"]
    
    # Görünüm için yuvarlama yap (Örn: 1.540000 -> 1.54)
    df["SONUÇ (Toplam Çarpan)"] = df["SONUÇ (Toplam Çarpan)"].round(2)

    # 2. MATPLOTLIB İLE GÖRSELLEŞTİRME
    fig, ax = plt.subplots(figsize=(12, 6)) # Tablo boyutunu ayarla
    
    # Eksenleri gizle (Sadece tablo görünsün)
    ax.axis('off')
    ax.set_title("Gym Pricing Engine - Decision Table", fontsize=16, weight='bold', pad=20)

    # Tabloyu oluştur
    table = ax.table(
        cellText=df.values, 
        colLabels=df.columns, 
        cellLoc='center', 
        loc='center',
        colColours=["#40466e"] * len(df.columns) # Başlık rengi
    )

    # 3. STİL AYARLARI
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 2) # (Genişlik, Yükseklik) ölçeği

    # Başlıkların metin rengini beyaz yap
    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(color='white', weight='bold')
            cell.set_edgecolor('white')
        else:
            # Satırları renklendir (Okunabilirlik için zebra stili)
            if row % 2 == 0:
                cell.set_facecolor('#f2f2f2')

    # 4. GÖSTER VE KAYDET
    plt.tight_layout()
    plt.savefig("decision_table_pricing.png", dpi=300, bbox_inches='tight') # Resmi kaydeder
    print("Tablo 'decision_table_pricing.png' olarak kaydedildi.")
    plt.show()

if __name__ == "__main__":
    generate_decision_table_image()