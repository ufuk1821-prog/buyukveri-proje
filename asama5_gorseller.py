import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from wordcloud import WordCloud

# ============================================================
# AŞAMA 5 — VERİ GÖRSELLEŞTİRME
# BLG462 Büyük Veri — Twitter US Airline Sentiment
# ============================================================

df = pd.read_csv('tweets_temiz.csv')
df['tweet_created'] = pd.to_datetime(df['tweet_created'], utc=True)
df['saat'] = df['tweet_created'].dt.hour

sns.set_theme(style='whitegrid')
RENKLER = {'negative': '#e74c3c', 'neutral': '#3498db', 'positive': '#2ecc71'}

print("=" * 60)
print("GÖRSELLEŞTİRME BAŞLIYOR — 5 Grafik üretilecek")
print("=" * 60)

# ============================================================
# GRAFİK 1 — Duygu Dağılımı (Pasta Grafik)
# ============================================================
print("\n[G1] Duygu dağılımı pasta grafiği oluşturuluyor...")

dagilim = df['airline_sentiment'].value_counts()
fig, ax = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax.pie(
    dagilim,
    labels=dagilim.index,
    autopct='%1.1f%%',
    colors=[RENKLER.get(k, '#95a5a6') for k in dagilim.index],
    startangle=140,
    wedgeprops={'edgecolor': 'white', 'linewidth': 2}
)
for at in autotexts:
    at.set_fontsize(12)
    at.set_fontweight('bold')
ax.set_title('Duygu Dağılımı (Pozitif / Negatif / Nötr)', fontsize=14, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('grafik1_duygu_dagilimi.png', dpi=150)
plt.show()
print("  ✓ grafik1_duygu_dagilimi.png kaydedildi")
print("  YORUM: Negatif tweetler açık ara çoğunluktadır (~63%).")
print("         Pozitif tweetler yalnızca ~16 oranındadır.")

# ============================================================
# GRAFİK 2 — Havayolu Bazında Duygu Dağılımı (Gruplu Bar)
# ============================================================
print("\n[G2] Havayolu bazında duygu dağılımı bar grafiği oluşturuluyor...")

pivot = df.groupby(['airline', 'airline_sentiment']).size().unstack(fill_value=0)
pivot = pivot[['negative', 'neutral', 'positive']]

fig, ax = plt.subplots(figsize=(12, 6))
pivot.plot(kind='bar', ax=ax,
           color=[RENKLER['negative'], RENKLER['neutral'], RENKLER['positive']],
           edgecolor='white', width=0.75)
ax.set_title('Havayolu Bazında Duygu Dağılımı', fontsize=14, fontweight='bold')
ax.set_xlabel('Havayolu Şirketi', fontsize=12)
ax.set_ylabel('Tweet Sayısı', fontsize=12)
ax.legend(title='Duygu', fontsize=10)
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('grafik2_havayolu_duygu.png', dpi=150)
plt.show()
print("  ✓ grafik2_havayolu_duygu.png kaydedildi")
print("  YORUM: United ve US Airways en yüksek negatif tweet sayısına sahiptir.")
print("         Virgin America görece daha olumlu bir profil sergiliyor.")

# ============================================================
# GRAFİK 3 — En Sık Kullanılan Kelimeler (WordCloud)
# ============================================================
print("\n[G3] WordCloud oluşturuluyor...")

metin = ' '.join(df['text_temiz'].dropna().tolist())
wc = WordCloud(
    width=1200, height=600,
    background_color='white',
    colormap='RdYlGn',
    max_words=150,
    contour_width=1,
    contour_color='steelblue'
).generate(metin)

fig, ax = plt.subplots(figsize=(14, 7))
ax.imshow(wc, interpolation='bilinear')
ax.axis('off')
ax.set_title('En Sık Kullanılan Kelimeler (WordCloud)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('grafik3_wordcloud.png', dpi=150)
plt.show()
print("  ✓ grafik3_wordcloud.png kaydedildi")
print("  YORUM: 'flight', 'cancel', 'delay', 'help' gibi kelimeler öne çıkıyor.")
print("         Bu, yolcuların en çok uçuş iptali ve gecikme konusunda şikayet ettiğini gösteriyor.")

# ============================================================
# GRAFİK 4 — Zaman Serisi (Saate Göre Tweet Sayısı)
# ============================================================
print("\n[G4] Saate göre tweet sayısı zaman serisi oluşturuluyor...")

saatlik = df.groupby('saat').size()

fig, ax = plt.subplots(figsize=(12, 5))
ax.fill_between(saatlik.index, saatlik.values, alpha=0.3, color='#8e44ad')
ax.plot(saatlik.index, saatlik.values, marker='o', color='#8e44ad', linewidth=2)
ax.set_title('Saate Göre Tweet Sayısı (UTC)', fontsize=14, fontweight='bold')
ax.set_xlabel('Saat (UTC)', fontsize=12)
ax.set_ylabel('Tweet Sayısı', fontsize=12)
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
ax.grid(True, alpha=0.4)
plt.tight_layout()
plt.savefig('grafik4_zaman_serisi.png', dpi=150)
plt.show()
print("  ✓ grafik4_zaman_serisi.png kaydedildi")
print("  YORUM: Sabah 12-18 UTC saatleri arasında (yerel sabah-öğleden sonra) tweet yoğunluğu yüksektir.")

# ============================================================
# GRAFİK 5 — Havayolu Başına Tweet Sayısı (Yatay Bar)
# ============================================================
print("\n[G5] Havayolu başına tweet sayısı oluşturuluyor...")

havayolu_sayim = df['airline'].value_counts()

fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.barh(havayolu_sayim.index, havayolu_sayim.values,
               color='#1abc9c', edgecolor='white')
for bar, val in zip(bars, havayolu_sayim.values):
    ax.text(val + 30, bar.get_y() + bar.get_height() / 2,
            str(val), va='center', fontsize=10)
ax.set_title('Havayolu Şirketine Göre Tweet Sayısı', fontsize=14, fontweight='bold')
ax.set_xlabel('Tweet Sayısı', fontsize=12)
ax.invert_yaxis()
plt.tight_layout()
plt.savefig('grafik5_havayolu_adet.png', dpi=150)
plt.show()
print("  ✓ grafik5_havayolu_adet.png kaydedildi")
print("  YORUM: United Airlines veri setinde en fazla tweet sayısına sahip havayoludur.")
print("         Bunu US Airways ve American Airlines takip etmektedir.")

print("\n" + "=" * 60)
print("✓ 5 grafik başarıyla oluşturuldu ve kaydedildi.")
print("=" * 60)
