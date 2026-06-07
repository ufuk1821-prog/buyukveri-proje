import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

df = pd.read_csv('tweets_temiz.csv')

plt.figure(figsize=(6,6))
df['airline_sentiment'].value_counts().plot.pie(autopct='%1.1f%%', colors=['#e74c3c','#2ecc71','#3498db'])
plt.title('Duygu Dağılımı')
plt.ylabel('')
plt.tight_layout()
plt.savefig('grafik1_duygu_dagilimi.png', dpi=150)
plt.show()

plt.figure(figsize=(10,5))
df.groupby('airline')['airline_sentiment'].value_counts().unstack().plot(kind='bar', figsize=(10,5), color=['#e74c3c','#2ecc71','#3498db'])
plt.title('Havayolu Bazında Duygu Dağılımı')
plt.xlabel('Havayolu')
plt.ylabel('Tweet Sayısı')
plt.tight_layout()
plt.savefig('grafik2_havayolu_duygu.png', dpi=150)
plt.show()

metin = ' '.join(df['text_temiz'].dropna().tolist())
wc = WordCloud(width=800, height=400, background_color='white').generate(metin)
plt.figure(figsize=(12,6))
plt.imshow(wc, interpolation='bilinear')
plt.axis('off')
plt.title('En Sık Kullanılan Kelimeler')
plt.tight_layout()
plt.savefig('grafik3_wordcloud.png', dpi=150)
plt.show()

df['tweet_created'] = pd.to_datetime(df['tweet_created'], utc=True)
df['saat'] = df['tweet_created'].dt.hour
plt.figure(figsize=(10,5))
df.groupby('saat').size().plot(kind='line', marker='o', color='#8e44ad')
plt.title('Saate Göre Tweet Sayısı')
plt.xlabel('Saat')
plt.ylabel('Tweet Sayısı')
plt.tight_layout()
plt.savefig('grafik4_zaman_serisi.png', dpi=150)
plt.show()

plt.figure(figsize=(8,5))
df['airline'].value_counts().plot(kind='bar', color='#1abc9c')
plt.title('Havayolu Başına Tweet Sayısı')
plt.xlabel('Havayolu')
plt.ylabel('Adet')
plt.tight_layout()
plt.savefig('grafik5_havayolu_adet.png', dpi=150)
plt.show()

print("5 grafik kaydedildi.")