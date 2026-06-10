import pandas as pd
 
df = pd.read_csv('Tweets.csv', encoding='latin-1')
 
print("=" * 50)
print(f"BOYUT: {df.shape[0]} satır, {df.shape[1]} sütun")
print("=" * 50)
 
print("\nSÜTUNLAR VE VERİ TİPLERİ:")
print(df.dtypes.to_string())
 
print("\nEKSİK DEĞERLER:")
print(df.isnull().sum().to_string())
 
print("\nSAYISAL SÜTUN İSTATİSTİKLERİ:")
print(df[['airline_sentiment_confidence', 'negativereason_confidence', 'retweet_count']].describe().to_string())
 
print("\nDUYGU DAĞILIMI:")
print(df['airline_sentiment'].value_counts().to_string())
 
print("\nHAVAYOLU DAĞILIMI:")
print(df['airline'].value_counts().to_string())
 
print("\nİLK 3 KAYIT (Seçili Sütunlar):")
print(df[['tweet_id', 'airline_sentiment', 'airline', 'text']].head(3).to_string())
 
print("\nVERİ SETİ BİLGİSİ:")
df.info()
 
print("=" * 50)