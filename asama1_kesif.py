import pandas as pd

# ============================================================
# AŞAMA 1 — VERİ TEMİNİ VE KEŞİF
# BLG462 Büyük Veri — Twitter US Airline Sentiment
# ============================================================

df = pd.read_csv('Tweets.csv', encoding='latin-1')

# --- 1.1 Boyut ve Sütunlar ---
print("=" * 60)
print("VERİ SETİ BOYUTU:")
print(f"  Satır sayısı : {df.shape[0]}")
print(f"  Sütun sayısı : {df.shape[1]}")

print("\nSÜTUN İSİMLERİ:")
for col in df.columns.tolist():
    print(f"  - {col}")

# --- 1.2 Veri Tipleri ---
print("\nVERİ TİPLERİ:")
print(df.dtypes)

# --- 1.3 Örnek Kayıtlar ---
print("\nİLK 5 KAYIT:")
print(df.head(5).to_string())

# --- 1.4 Temel İstatistikler ---
print("\nTEMEL İSTATİSTİKLER (describe):")
print(df.describe(include='all').to_string())

# --- 1.5 Genel Bilgi (info) ---
print("\nVERİ SETİ BİLGİSİ (info):")
df.info()

# --- 1.6 Duygu Etiketi Dağılımı ---
print("\nDUYGU ETİKETİ DAĞILIMI:")
print(df['airline_sentiment'].value_counts())
print(df['airline_sentiment'].value_counts(normalize=True).mul(100).round(2).astype(str) + ' %')

print("\nHAVAYOLU DAĞILIMI:")
print(df['airline'].value_counts())

print("\nEKSİK DEĞER SAYILARI:")
print(df.isnull().sum())

print("\n" + "=" * 60)
print("DIKW PİRAMİDİ DEĞERLENDİRMESİ:")
print("""
  DATA    (Veri)      : Ham tweet metinleri, zaman damgaları, kullanıcı adları
  INFORMATION (Bilgi) : Duygu etiketleri, havayolu bazlı dağılımlar, güven skorları
  KNOWLEDGE (Anlam)   : Hangi havayolu daha çok olumsuz yorum alıyor?
                        Hangi saatlerde şikayet yoğunluğu artıyor?
  WISDOM  (Bilgelik)  : Havayolu şirketleri bu veriden müşteri memnuniyeti
                        stratejisi geliştirebilir; kriz saatlerini önceden tespit edebilir.
""")
print("=" * 60)
