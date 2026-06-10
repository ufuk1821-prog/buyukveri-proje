import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from wordcloud import WordCloud

df = pd.read_csv('tweets_temiz.csv')
df['tweet_created'] = pd.to_datetime(df['tweet_created'], utc=True)
df['saat'] = df['tweet_created'].dt.hour
sns.set_theme(style='whitegrid')
RENKLER = {'negative': '#e74c3c', 'neutral': '#3498db', 'positive': '#2ecc71'}

dagilim = df['airline_sentiment'].value_counts()
fig, ax = plt.subplots(figsize=(7, 7))
ax.pie(dagilim, labels=dagilim.index, autopct='%1.1f%%',
       colors=[RENKLER[k] for k in dagilim.index],
       startangle=140, wedgeprops={'edgecolor': 'white', 'linewidth': 2})
ax.set_title('Duygu Dağılımı', fontsize=14, fontweight='bold')
plt.tight_layout(); plt.savefig('grafik1_duygu_dagilimi.png', dpi=150); plt.show()
print("grafik1 kaydedildi.")

pivot = df.groupby(['airline', 'airline_sentiment']).size().unstack(fill_value=0)[['negative', 'neutral', 'positive']]
fig, ax = plt.subplots(figsize=(12, 6))
pivot.plot(kind='bar', ax=ax, color=[RENKLER['negative'], RENKLER['neutral'], RENKLER['positive']], edgecolor='white', width=0.75)
ax.set_title('Havayolu Bazında Duygu Dağılımı', fontsize=14, fontweight='bold')
ax.set_xlabel('Havayolu'); ax.set_ylabel('Tweet Sayısı')
plt.xticks(rotation=30, ha='right'); plt.tight_layout(); plt.savefig('grafik2_havayolu_duygu.png', dpi=150); plt.show()
print("grafik2 kaydedildi.")

wc = WordCloud(width=1200, height=600, background_color='white', colormap='RdYlGn', max_words=150).generate(' '.join(df['text_temiz'].dropna()))
fig, ax = plt.subplots(figsize=(14, 7))
ax.imshow(wc, interpolation='bilinear'); ax.axis('off')
ax.set_title('En Sık Kullanılan Kelimeler', fontsize=14, fontweight='bold')
plt.tight_layout(); plt.savefig('grafik3_wordcloud.png', dpi=150); plt.show()
print("grafik3 kaydedildi.")

saatlik = df.groupby('saat').size()
fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(saatlik.index, saatlik.values, alpha=0.3, color='#8e44ad')
ax.plot(saatlik.index, saatlik.values, marker='o', color='#8e44ad', linewidth=2)
ax.set_title('Saate Göre Tweet Sayısı (UTC)', fontsize=14, fontweight='bold')
ax.set_xlabel('Saat'); ax.set_ylabel('Tweet Sayısı')
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
plt.tight_layout(); plt.savefig('grafik4_zaman_serisi.png', dpi=150); plt.show()
print("grafik4 kaydedildi.")

sayim = df['airline'].value_counts()
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(sayim.index, sayim.values, color='#1abc9c', edgecolor='white')
for bar, val in zip(bars, sayim.values):
    ax.text(val + 30, bar.get_y() + bar.get_height() / 2, str(val), va='center', fontsize=10)
ax.set_title('Havayoluna Göre Tweet Sayısı', fontsize=14, fontweight='bold')
ax.set_xlabel('Tweet Sayısı'); ax.invert_yaxis()
plt.tight_layout(); plt.savefig('grafik5_havayolu_adet.png', dpi=150); plt.show()
print("grafik5 kaydedildi.")
