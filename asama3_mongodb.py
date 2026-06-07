import pandas as pd
from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://ufuk1821_db_user:MMuAW2BhrTo5Guve@cluster0.eaqxovk.mongodb.net/?appName=Cluster0"

client = MongoClient(uri)
db = client['twitter_db']
collection = db['tweetler']

df = pd.read_csv('tweets_temiz.csv')

collection.drop()

kayitlar = df.to_dict(orient='records')
collection.insert_many(kayitlar)

print("Yüklenen kayıt:", collection.count_documents({}))

print("\n--- find() Sorguları ---")

print(list(collection.find({'airline_sentiment': 'negative'}, {'text_temiz': 1, 'airline': 1, '_id': 0}).limit(3)))

print(list(collection.find({'airline': 'United'}, {'text_temiz': 1, '_id': 0}).limit(3)))

print(list(collection.find({'airline_sentiment_confidence': {'$gt': 0.9}}, {'text_temiz': 1, '_id': 0}).limit(3)))

print("\n--- Aggregation ---")

pipeline1 = [
    {'$group': {'_id': '$airline_sentiment', 'adet': {'$sum': 1}}},
    {'$sort': {'adet': -1}}
]
print(list(collection.aggregate(pipeline1)))

pipeline2 = [
    {'$group': {'_id': '$airline', 'ortalama_guven': {'$avg': '$airline_sentiment_confidence'}}},
    {'$sort': {'ortalama_guven': -1}}
]
print(list(collection.aggregate(pipeline2)))

pipeline3 = [
    {'$match': {'airline_sentiment': 'negative'}},
    {'$group': {'_id': '$airline', 'negatif_adet': {'$sum': 1}}},
    {'$sort': {'negatif_adet': -1}}
]
print(list(collection.aggregate(pipeline3)))

print("\n--- İndeks ---")
collection.create_index('airline_sentiment')
print("İndeks oluşturuldu")

print("\n--- Update ---")
collection.update_many({'airline_sentiment': 'neutral'}, {'$set': {'etiket': 'nötr'}})
print("update_many tamamlandı")
collection.update_one({'airline': 'Delta'}, {'$inc': {'airline_sentiment_confidence': 0.01}})
print("update_one tamamlandı")

print("\n--- Delete ---")
sonuc = collection.delete_many({'text_temiz': ''})
print("Silinen:", sonuc.deleted_count)

print("\n--- İleri Sorgular ---")
print(list(collection.find({'text_temiz': {'$regex': 'delay'}}, {'text_temiz': 1, '_id': 0}).limit(3)))
print(list(collection.find({'negativereason': {'$exists': True, '$ne': None}}, {'negativereason': 1, '_id': 0}).limit(3)))