import pandas as pd
import re

# ============================================================
# AŞAMA 2 — VERİ TEMİZLEME VE HAZIRLIK
# BLG462 Büyük Veri — Twitter US Airline Sentiment
# ============================================================

df = pd.read_csv('Tweets.csv', encoding='latin-1')

print("=" * 60)
print(f"TEMİZLEME ÖNCESİ KAYIT SAYISI: {len(df)}")
print("=" * 60)

# --- 2.1 Eksik Değer Tespiti ---
print("\nEKSİK DEĞER ANALİZİ (Temizleme Öncesi):")
print(df.isnull().sum())
print(f"\nToplam eksik hücre: {df.isnull().sum().sum()}")

# --- 2.2 Duplicate Tespiti ---
print(f"\nTEKRARLANAN KAYIT SAYISI: {df.duplicated().sum()}")

# --- 2.3 Metin Temizleme Fonksiyonu ---
def temizle(metin):
    """URL, mention, hashtag ve özel karakterleri temizler."""
    if pd.isna(metin):
        return ""
    metin = re.sub(r'http\S+', '', metin)       # URL temizle
    metin = re.sub(r'@\w+', '', metin)           # @mention temizle
    metin = re.sub(r'#\w+', '', metin)           # #hashtag temizle
    metin = re.sub(r'[^a-zA-Z\s]', '', metin)   # Özel karakter temizle
    metin = metin.lower().strip()
    metin = re.sub(r'\s+', ' ', metin)           # Çoklu boşluk temizle
    return metin

print("\nMETİN TEMİZLEME UYGULANIYORU...")
df['text_temiz'] = df['text'].apply(temizle)
print("  ✓ URL'ler temizlendi")
print("  ✓ @mention'lar temizlendi")
print("  ✓ #hashtag'ler temizlendi")
print("  ✓ Özel karakterler temizlendi")

# Örnek karşılaştırma
print("\nÖRNEK TEMİZLEME KARŞILAŞTIRMASI (ilk 3 kayıt):")
for i in range(3):
    print(f"\n  Ham    : {df['text'].iloc[i]}")
    print(f"  Temiz  : {df['text_temiz'].iloc[i]}")

# --- 2.4 Eksik Değerleri Giderme ---
print("\nEKSİK DEĞER GİDERME:")
önce = len(df)
df.dropna(subset=['airline_sentiment', 'text'], inplace=True)
print(f"  airline_sentiment veya text eksik olan {önce - len(df)} kayıt silindi.")

# negativereason eksiklerini 'Unknown' ile doldur
df['negativereason'] = df['negativereason'].fillna('Unknown')
df['negativereason_confidence'] = df['negativereason_confidence'].fillna(0.0)
print("  negativereason eksikleri 'Unknown' ile dolduruldu.")

# --- 2.5 Duplicate Silme ---
önce_dup = len(df)
df.drop_duplicates(inplace=True)
print(f"\nDUPLICATE SİLME: {önce_dup - len(df)} tekrarlanan kayıt silindi.")

# --- 2.6 Veri Tipi Dönüşümleri ---
print("\nVERİ TİPİ DÖNÜŞÜMÜ:")
df['tweet_created'] = pd.to_datetime(df['tweet_created'], utc=True)
df['tweet_id'] = df['tweet_id'].astype(str)
df['airline_sentiment_confidence'] = pd.to_numeric(df['airline_sentiment_confidence'], errors='coerce')
print("  tweet_created → datetime (UTC)")
print("  tweet_id       → string")
print("  airline_sentiment_confidence → float")

# --- 2.7 Sütun Tipi Doğrulama ---
print("\nGÜNCELLENMİŞ VERİ TİPLERİ:")
print(df.dtypes)

# --- 2.8 Veri Kalitesi Değerlendirmesi ---
print("\n" + "=" * 60)
print("VERİ KALİTESİ BOYUTLARI:")
print(f"""
  1. DOĞRULUK (Accuracy)   : airline_sentiment sütunu yalnızca
                             'positive', 'negative', 'neutral' içeriyor.
                             Geçersiz etiket sayısı: {df[~df['airline_sentiment'].isin(['positive','negative','neutral'])].shape[0]}

  2. TAMLIK (Completeness) : Kritik sütunlarda (airline_sentiment, text)
                             eksik değer kalmadı. Eksik satırlar silindi.

  3. TUTARLILIK (Consistency): tweet_created tüm kayıtlarda UTC datetime
                             formatına dönüştürüldü, tip tutarlılığı sağlandı.
""")

# --- 2.9 Karşılaştırmalı Özet ---
print("=" * 60)
print("TEMİZLEME ÖZET RAPORU:")
print(f"  Önceki kayıt sayısı : {önce}")
print(f"  Sonraki kayıt sayısı: {len(df)}")
print(f"  Silinen kayıt       : {önce - len(df)}")
print("=" * 60)

# Temizlenmiş veriyi kaydet
df.to_csv('tweets_temiz.csv', index=False)
print("\n✓ Temizlenmiş veri 'tweets_temiz.csv' olarak kaydedildi.")
