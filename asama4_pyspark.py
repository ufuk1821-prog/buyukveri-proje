import os
os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-17.0.2'
 
import time
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, lower, trim
 
spark = SparkSession.builder.appName('TwitterAnalysis').config("spark.sql.shuffle.partitions", "4").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
 
df = spark.read.csv('tweets_temiz.csv', header=True, inferSchema=False)
df = df.filter(col('airline_sentiment').isin('negative', 'neutral', 'positive'))
df = df.withColumn('guven', when(col('airline_sentiment_confidence').rlike(r'^[0-9.]+$'), col('airline_sentiment_confidence').cast('float')).otherwise(None))
 
print("=" * 50)
print("PYSPARK OTURUMU BAŞLADI")
print("=" * 50)
 
print("\n--- Dönüşümler (Transformations) ---")
 
print("\n[T1] select():")
df.select('tweet_id', 'airline_sentiment', 'airline', 'guven', 'text_temiz').show(5, truncate=50)
 
print("\n[T2] filter() + withColumn():")
df.filter((col('airline_sentiment') == 'negative') & (col('airline') == 'United')) \
  .withColumn('text_kucuk', lower(trim(col('text_temiz')))) \
  .select('airline', 'airline_sentiment', 'text_kucuk').show(5, truncate=60)
 
print("\n[T3] groupBy():")
df.filter(col('airline_sentiment').isin('negative', 'neutral', 'positive')) \
  .groupBy('airline', 'airline_sentiment').count().orderBy('airline').show(18)
 
print("\n--- Eylemler (Actions) ---")
print(f"\n[E1] count(): {df.count()}")
print("\n[E2] describe():")
df.select('guven').describe().show()
print("\n[E3] collect() — ilk 3 kayıt:")
for r in df.select('airline', 'airline_sentiment', 'guven').limit(3).collect():
    print(f"  {r}")
print("\n[E4] show() — duygu dağılımı:")
df.groupBy('airline_sentiment').count().orderBy('count', ascending=False).show()
 
print("\n--- Spark SQL ---")
df.createOrReplaceTempView('tweetler')
 
print("\n[SQL1] Havayolu bazında negatif tweet sayısı:")
spark.sql("SELECT airline, COUNT(*) AS negatif FROM tweetler WHERE airline_sentiment='negative' GROUP BY airline ORDER BY negatif DESC").show()
 
print("\n[SQL2] Güven > 0.9 olan duygu dağılımı:")
spark.sql("SELECT airline_sentiment, COUNT(*) AS adet, ROUND(AVG(CAST(guven AS FLOAT)),3) AS ort_guven FROM tweetler WHERE guven > 0.9 GROUP BY airline_sentiment ORDER BY adet DESC").show()
 
print("\n--- Pandas vs PySpark Karşılaştırması ---")
t1 = time.time(); pd.read_csv('tweets_temiz.csv').groupby('airline_sentiment').size(); t2 = time.time()
t3 = time.time(); df.groupBy('airline_sentiment').count().collect(); t4 = time.time()
print(f"\n[K1] Pandas süresi : {round(t2-t1, 4)} saniye")
print(f"[K2] PySpark süresi: {round(t4-t3, 4)} saniye")
 
print("\n" + "=" * 50)
print("PySpark aşaması tamamlandı.")
print("=" * 50)
spark.stop()