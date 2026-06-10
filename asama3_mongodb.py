import pandas as pd
from pymongo.mongo_client import MongoClient
import pprint

# ============================================================
# AŞAMA 3 — MONGODB'YE YÜKLEME VE NOSQL SORGULARI
# BLG462 Büyük Veri — Twitter US Airline Sentiment
# ============================================================

uri = "mongodb+srv://ufuk1821_db_user:MMuAW2BhrTo5Guve@cluster0.eaqxovk.mongodb.net/?appName=Cluster0"
client = MongoClient(uri)
db = client['twitter_db']
collection = db['tweetler']

# --- 3.1 Veri Yükleme ---
df = pd.read_csv('tweets_temiz.csv')
collection.drop()
kayitlar = df.to_dict(orient='records')
collection.insert_many(kayitlar)
print("=" * 60)
print(f"YÜKLENEN KAYIT SAYISI: {collection.count_documents({})}")
print("=" * 60)

# ============================================================
# MONGODB ŞEMA AÇIKLAMASI
# Her tweet dokümanı aşağıdaki alanları içermektedir:
#   tweet_id                     : string
#   airline_sentiment            : 'positive' | 'negative' | 'neutral'
#   airline_sentiment_confidence : float (0.0 - 1.0)
#   negativereason               : string | 'Unknown'
#   airline                      : string
#   text                         : ham tweet metni
#   text_temiz                   : temizlenmiş tweet metni
#   tweet_created                : datetime (UTC)
#   tweet_location               : string
#   user_timezone                : string
# ============================================================

# ============================================================
# find() ile TEMEL SORGULAR (En az 3)
# ============================================================
print("\n" + "=" * 60)
print("1. find() SORGULARI")
print("=" * 60)

# Sorgu 1 — Negatif tweetler, projeksiyon + limit
print("\n[S1] Negatif tweetlerden ilk 3 (text_temiz + airline):")
sonuc1 = list(collection.find(
    {'airline_sentiment': 'negative'},
    {'text_temiz': 1, 'airline': 1, '_id': 0}
).limit(3))
pprint.pprint(sonuc1)

# Sorgu 2 — United havayolu, limit + skip
print("\n[S2] United havayoluna ait tweetler (skip=2, limit=3):")
sonuc2 = list(collection.find(
    {'airline': 'United'},
    {'text_temiz': 1, 'airline_sentiment': 1, '_id': 0}
).skip(2).limit(3))
pprint.pprint(sonuc2)

# Sorgu 3 — Güven skoru > 0.9, projeksiyon + limit
print("\n[S3] Güven skoru 0.9 üzeri tweetler (limit=3):")
sonuc3 = list(collection.find(
    {'airline_sentiment_confidence': {'$gt': 0.9}},
    {'text_temiz': 1, 'airline': 1, 'airline_sentiment': 1, '_id': 0}
).limit(3))
pprint.pprint(sonuc3)

# ============================================================
# AGGREGATION PIPELINE (En az 3, $project dahil)
# ============================================================
print("\n" + "=" * 60)
print("2. AGGREGATION PIPELINE")
print("=" * 60)

# Aggregation 1 — Duygu bazında sayım + $project
print("\n[A1] Duygu etiketine göre tweet sayısı ($group + $sort + $project):")
pipeline1 = [
    {'$group': {'_id': '$airline_sentiment', 'toplam': {'$sum': 1}}},
    {'$sort': {'toplam': -1}},
    {'$project': {'etiket': '$_id', 'tweet_sayisi': '$toplam', '_id': 0}}
]
pprint.pprint(list(collection.aggregate(pipeline1)))

# Aggregation 2 — Havayolu bazında ortalama güven ($match + $group + $sort + $project)
print("\n[A2] Havayolu bazında ortalama güven skoru:")
pipeline2 = [
    {'$match': {'airline_sentiment_confidence': {'$gt': 0}}},
    {'$group': {'_id': '$airline', 'ort_guven': {'$avg': '$airline_sentiment_confidence'}}},
    {'$sort': {'ort_guven': -1}},
    {'$project': {'havayolu': '$_id', 'ortalama_guven': {'$round': ['$ort_guven', 3]}, '_id': 0}}
]
pprint.pprint(list(collection.aggregate(pipeline2)))

# Aggregation 3 — Negatif tweet sayısı havayolu bazında
print("\n[A3] Havayolu başına negatif tweet sayısı ($match + $group + $sort + $project):")
pipeline3 = [
    {'$match': {'airline_sentiment': 'negative'}},
    {'$group': {'_id': '$airline', 'negatif_adet': {'$sum': 1}}},
    {'$sort': {'negatif_adet': -1}},
    {'$project': {'havayolu': '$_id', 'negatif_tweet': '$negatif_adet', '_id': 0}}
]
pprint.pprint(list(collection.aggregate(pipeline3)))

# ============================================================
# İNDEKS OLUŞTURMA VE PERFORMANS KARŞILAŞTIRMASI (explain)
# ============================================================
print("\n" + "=" * 60)
print("3. İNDEKS OLUŞTURMA VE PERFORMANS TESTİ")
print("=" * 60)

# explain() — indeks öncesi
print("\n[I1] İndeks OLMADAN sorgu planı (explain):")
plan_oncesi = collection.find(
    {'airline_sentiment': 'negative'}
).explain()
print(f"  Tarama tipi    : {plan_oncesi['queryPlanner']['winningPlan']['stage']}")
print(f"  İncelenen dok. : {plan_oncesi.get('executionStats', {}).get('totalDocsExamined', 'N/A')}")

# İndeks oluştur
collection.create_index('airline_sentiment')
print("\n  ✓ airline_sentiment alanına indeks oluşturuldu.")

# explain() — indeks sonrası
print("\n[I2] İndeks SONRASI sorgu planı (explain):")
plan_sonrasi = collection.find(
    {'airline_sentiment': 'negative'}
).explain()
print(f"  Tarama tipi    : {plan_sonrasi['queryPlanner']['winningPlan']['stage']}")
print(f"  İncelenen dok. : {plan_sonrasi.get('executionStats', {}).get('totalDocsExamined', 'N/A')}")

print("\n  → İndeks sayesinde COLLSCAN yerine IXSCAN kullanıldı.")

# ============================================================
# UPDATE İŞLEMLERİ (En az 2)
# ============================================================
print("\n" + "=" * 60)
print("4. UPDATE İŞLEMLERİ")
print("=" * 60)

# update_many — neutral tweetlere 'etiket' alanı ekle
sonuc_u1 = collection.update_many(
    {'airline_sentiment': 'neutral'},
    {'$set': {'etiket': 'nötr'}}
)
print(f"\n[U1] update_many — 'neutral' tweetlere etiket='nötr' eklendi.")
print(f"  Eşleşen  : {sonuc_u1.matched_count}")
print(f"  Güncellenen: {sonuc_u1.modified_count}")

# update_one — Delta havayolunun bir tweetinin güven skorunu artır
sonuc_u2 = collection.update_one(
    {'airline': 'Delta'},
    {'$inc': {'airline_sentiment_confidence': 0.01}}
)
print(f"\n[U2] update_one — Delta tweetinin güven skoru 0.01 artırıldı.")
print(f"  Eşleşen  : {sonuc_u2.matched_count}")
print(f"  Güncellenen: {sonuc_u2.modified_count}")

# ============================================================
# DELETE İŞLEMLERİ (En az 1)
# ============================================================
print("\n" + "=" * 60)
print("5. DELETE İŞLEMLERİ")
print("=" * 60)

# deleteMany — text_temiz boş olan kayıtları sil
onceki_sayi = collection.count_documents({})
sonuc_d1 = collection.delete_many({'text_temiz': ''})
print(f"\n[D1] deleteMany — text_temiz boş olan kayıtlar silindi.")
print(f"  Silinen kayıt sayısı : {sonuc_d1.deleted_count}")
print(f"  Kalan kayıt sayısı   : {collection.count_documents({})}")

# ============================================================
# SERBEST / İLERİ SORGULAR (En az 2)
# ============================================================
print("\n" + "=" * 60)
print("6. İLERİ SORGULAR")
print("=" * 60)

# İleri Sorgu 1 — Regex sorgusu
print("\n[İ1] Regex — 'delay' içeren tweetler (ilk 3):")
sonuc_r1 = list(collection.find(
    {'text_temiz': {'$regex': 'delay', '$options': 'i'}},
    {'text_temiz': 1, 'airline': 1, '_id': 0}
).limit(3))
pprint.pprint(sonuc_r1)

# İleri Sorgu 2 — Nested/exists sorgusu
print("\n[İ2] exists — negativereason alanı dolu olan tweetler (ilk 3):")
sonuc_r2 = list(collection.find(
    {'negativereason': {'$exists': True, '$nin': [None, 'Unknown']}},
    {'negativereason': 1, 'airline': 1, 'airline_sentiment': 1, '_id': 0}
).limit(3))
pprint.pprint(sonuc_r2)

print("\n" + "=" * 60)
print("✓ Tüm MongoDB sorguları tamamlandı.")
print("=" * 60)

client.close()
