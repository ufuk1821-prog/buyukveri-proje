import os
os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-17.0.2'

import time
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, when

spark = SparkSession.builder.appName('TwitterAnalysis').getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

df_spark = spark.read.csv('tweets_temiz.csv', header=True, inferSchema=False)

df_spark = df_spark.withColumn(
    'guven',
    when(col('airline_sentiment_confidence').rlike('^[0-9.]+$'),
         col('airline_sentiment_confidence').cast('float')).otherwise(None)
)

print("Şema:")
df_spark.printSchema()

print("\nİlk 5 satır:")
df_spark.select('tweet_id','airline_sentiment','airline','guven','text_temiz').show(5)

print("\nToplam kayıt:", df_spark.count())

print("\nDuygu dağılımı:")
df_spark.filter(col('airline_sentiment').isin('negative','neutral','positive')) \
    .groupBy('airline_sentiment').count().orderBy('count', ascending=False).show()

print("\nHavayolu bazında ortalama güven:")
df_spark.groupBy('airline').agg(avg('guven').alias('ort_guven')).show()

print("\nNegatif United tweetleri:")
df_spark.filter((col('airline_sentiment') == 'negative') & (col('airline') == 'United')) \
    .select('text_temiz').show(5)

df_spark.createOrReplaceTempView('tweetler')

print("\nSpark SQL - Havayolu bazında negatif sayı:")
spark.sql("SELECT airline, COUNT(*) as negatif FROM tweetler WHERE airline_sentiment='negative' GROUP BY airline ORDER BY negatif DESC").show()

print("\nSpark SQL - Güven > 0.9 olanlar:")
spark.sql("SELECT airline_sentiment, COUNT(*) as adet FROM tweetler WHERE guven > 0.9 GROUP BY airline_sentiment").show()

print("\n--- Pandas vs PySpark Karşılaştırma ---")

t1 = time.time()
df_pd = pd.read_csv('tweets_temiz.csv')
df_pd.groupby('airline_sentiment').size()
t2 = time.time()
print(f"Pandas süresi: {round(t2-t1, 4)} saniye")

t3 = time.time()
df_spark.groupBy('airline_sentiment').count().collect()
t4 = time.time()
print(f"PySpark süresi: {round(t4-t3, 4)} saniye")

spark.stop()