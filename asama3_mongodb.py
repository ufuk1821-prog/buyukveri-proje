import pandas as pd
from pymongo.mongo_client import MongoClient
import pprint

uri = "mongodb+srv://ufuk1821_db_user:MMuAW2BhrTo5Guve@cluster0.eaqxovk.mongodb.net/?appName=Cluster0"
client = MongoClient(uri, serverSelectionTimeoutMS=20000, connectTimeoutMS=20000, socketTimeoutMS=60000)
client.admin.command('ping')
db = client['twitter_db']
collection = db['tweetler']

df = pd.read_csv('tweets_temiz.csv')
collection.drop()
kayitlar = df.to_dict(orient='records')
for i in range(0, len(kayitlar), 1000):
    collection.insert_many(kayitlar[i:i+1000])

print("=" * 50)
print(f"YÜKLENEN KAYIT SAYISI: {collection.count_documents({})}")
print("=" * 50)

print("\n--- find() Sorguları ---")
print("\n[S1] Negatif tweetler (limit=3):")
pprint.pprint(list(collection.find({'airline_sentiment': 'negative'}, {'text_temiz': 1, 'airline': 1, '_id': 0}).limit(3)))

print("\n[S2] United tweetleri (skip=2, limit=3):")
pprint.pprint(list(collection.find({'airline': 'United'}, {'text_temiz': 1, 'airline_sentiment': 1, '_id': 0}).skip(2).limit(3)))

print("\n[S3] Güven skoru > 0.9 (limit=3):")
pprint.pprint(list(collection.find({'airline_sentiment_confidence': {'$gt': 0.9}}, {'text_temiz': 1, 'airline': 1, '_id': 0}).limit(3)))

print("\n--- Aggregation Pipeline ---")
print("\n[A1] Duygu bazında tweet sayısı:")
pprint.pprint(list(collection.aggregate([
    {'$group': {'_id': '$airline_sentiment', 'toplam': {'$sum': 1}}},
    {'$sort': {'toplam': -1}},
    {'$project': {'etiket': '$_id', 'tweet_sayisi': '$toplam', '_id': 0}}
])))

print("\n[A2] Havayolu bazında ortalama güven skoru:")
pprint.pprint(list(collection.aggregate([
    {'$match': {'airline_sentiment_confidence': {'$gt': 0}}},
    {'$group': {'_id': '$airline', 'ort': {'$avg': '$airline_sentiment_confidence'}}},
    {'$sort': {'ort': -1}},
    {'$project': {'havayolu': '$_id', 'ort_guven': {'$round': ['$ort', 3]}, '_id': 0}}
])))

print("\n[A3] Havayolu başına negatif tweet sayısı:")
pprint.pprint(list(collection.aggregate([
    {'$match': {'airline_sentiment': 'negative'}},
    {'$group': {'_id': '$airline', 'adet': {'$sum': 1}}},
    {'$sort': {'adet': -1}},
    {'$project': {'havayolu': '$_id', 'negatif_tweet': '$adet', '_id': 0}}
])))

print("\n--- İndeks ve explain() ---")
plan1 = collection.find({'airline_sentiment': 'negative'}).explain()
print(f"\n[I1] İndeks öncesi tarama tipi : {plan1['queryPlanner']['winningPlan']['stage']}")
collection.create_index('airline_sentiment')
plan2 = collection.find({'airline_sentiment': 'negative'}).explain()
print(f"[I2] İndeks sonrası tarama tipi: {plan2['queryPlanner']['winningPlan']['stage']}")

print("\n--- Update ---")
r1 = collection.update_many({'airline_sentiment': 'neutral'}, {'$set': {'etiket': 'nötr'}})
print(f"\n[U1] update_many — eşleşen: {r1.matched_count}, güncellenen: {r1.modified_count}")
r2 = collection.update_one({'airline': 'Delta'}, {'$inc': {'airline_sentiment_confidence': 0.01}})
print(f"[U2] update_one  — eşleşen: {r2.matched_count}, güncellenen: {r2.modified_count}")

print("\n--- Delete ---")
r3 = collection.delete_many({'text_temiz': ''})
print(f"\n[D1] deleteMany — silinen: {r3.deleted_count}, kalan: {collection.count_documents({})}")

print("\n--- İleri Sorgular ---")
print("\n[İ1] Regex — 'delay' içeren tweetler:")
pprint.pprint(list(collection.find({'text_temiz': {'$regex': 'delay', '$options': 'i'}}, {'text_temiz': 1, 'airline': 1, '_id': 0}).limit(3)))

print("\n[İ2] exists — negativereason dolu olan tweetler:")
pprint.pprint(list(collection.find({'negativereason': {'$exists': True, '$nin': [None, 'Unknown']}}, {'negativereason': 1, 'airline': 1, '_id': 0}).limit(3)))

print("\n" + "=" * 50)
print("Tüm sorgular tamamlandı.")
print("=" * 50)
client.close()
