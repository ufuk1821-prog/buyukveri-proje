import pandas as pd
import re

df = pd.read_csv('Tweets.csv', encoding='latin-1')

print("Temizleme öncesi:", len(df))

def temizle(metin):
    if pd.isna(metin):
        return ""
    metin = re.sub(r'http\S+', '', metin)
    metin = re.sub(r'@\w+', '', metin)
    metin = re.sub(r'#\w+', '', metin)
    metin = re.sub(r'[^a-zA-Z\s]', '', metin)
    metin = metin.lower().strip()
    return metin

df['text_temiz'] = df['text'].apply(temizle)

print("Eksik değerler:")
print(df.isnull().sum())

df.dropna(subset=['airline_sentiment', 'text'], inplace=True)
df.drop_duplicates(inplace=True)

df['tweet_created'] = pd.to_datetime(df['tweet_created'], utc=True)

print("Temizleme sonrası:", len(df))

df.to_csv('tweets_temiz.csv', index=False)
print("Kaydedildi: tweets_temiz.csv")