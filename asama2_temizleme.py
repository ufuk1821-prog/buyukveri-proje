import pandas as pd
import re

df = pd.read_csv('Tweets.csv', encoding='latin-1')

print("=" * 50)
print(f"TEMİZLEME ÖNCESİ KAYIT SAYISI: {len(df)}")
print("=" * 50)
print(f"\nEKSİK DEĞERLER:\n{df.isnull().sum()}")
print(f"\nDUPLICATE SAYISI: {df.duplicated().sum()}")

def temizle(metin):
    if pd.isna(metin): return ""
    metin = re.sub(r'http\S+|@\w+|#\w+|[^a-zA-Z\s]', '', metin)
    return re.sub(r'\s+', ' ', metin).lower().strip()

df['text_temiz'] = df['text'].apply(temizle)
df.dropna(subset=['airline_sentiment', 'text'], inplace=True)
df['negativereason'] = df['negativereason'].fillna('Unknown')
df['negativereason_confidence'] = df['negativereason_confidence'].fillna(0.0)
df.drop_duplicates(inplace=True)
df['tweet_created'] = pd.to_datetime(df['tweet_created'], utc=True)
df['tweet_id'] = df['tweet_id'].astype(str)
df['airline_sentiment_confidence'] = pd.to_numeric(df['airline_sentiment_confidence'], errors='coerce')

print(f"\nGÜNCEL VERİ TİPLERİ:\n{df.dtypes}")
print("\n" + "=" * 50)
print(f"TEMİZLEME SONRASI KAYIT SAYISI: {len(df)}")
print("=" * 50)
df.to_csv('tweets_temiz.csv', index=False)
print("tweets_temiz.csv kaydedildi.")
