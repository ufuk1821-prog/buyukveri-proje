import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

fig, ax = plt.subplots(figsize=(10, 14))
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)
ax.axis('off')

kutular = [
    (5, 12.5, 'KAYNAK\nKaggle - Twitter US Airline Sentiment\n~14.000 Tweet, CSV Format', '#2980b9'),
    (5, 10.5, 'EXTRACT\nKaggle\'dan CSV İndirme\nAraç: Kaggle Web Arayüzü', '#8e44ad'),
    (5, 8.5, 'TRANSFORM 1\nPandas ile Veri Temizleme\nURL/mention/hashtag temizleme, duplicate silme\nAraç: Python, Pandas', '#27ae60'),
    (5, 6.5, 'TRANSFORM 2\nPySpark ile Dağıtık İşleme\nfilter(), groupBy(), Spark SQL\nAraç: PySpark, Java', '#e67e22'),
    (5, 4.5, 'LOAD\nMongoDB Atlas\'a Yükleme\n14.604 kayıt, bulk insert\nAraç: PyMongo, MongoDB Atlas', '#c0392b'),
    (5, 2.5, 'VİZUALİZASYON\nMatplotlib & Seaborn & WordCloud\n5 Grafik: Pasta, Bar, WordCloud, Zaman Serisi\nAraç: Matplotlib, Seaborn', '#16a085'),
]

for (x, y, metin, renk) in kutular:
    ax.add_patch(mpatches.FancyBboxPatch((x-3.5, y-0.7), 7, 1.4,
        boxstyle="round,pad=0.1", facecolor=renk, edgecolor='white', linewidth=2))
    ax.text(x, y, metin, ha='center', va='center', fontsize=8.5,
            color='white', fontweight='bold', multialignment='center')

oklar = [12.5, 10.5, 8.5, 6.5, 4.5]
for y in oklar:
    ax.annotate('', xy=(5, y-0.7), xytext=(5, y-1.3),
                arrowprops=dict(arrowstyle='->', color='#2c3e50', lw=2.5))

ax.text(5, 13.7, 'ETL Akış Diyagramı — Twitter Büyük Veri Pipeline',
        ha='center', va='center', fontsize=13, fontweight='bold', color='#2c3e50')

plt.tight_layout()
plt.savefig('etl_diyagram.png', dpi=150, bbox_inches='tight', facecolor='#ecf0f1')
plt.show()
print("etl_diyagram.png kaydedildi")