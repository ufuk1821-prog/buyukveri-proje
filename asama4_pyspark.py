import os
os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-17.0.2'

import time
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, when, count, lower, trim

# ============================================================
# AŞAMA 4 — PYSPARK İLE DAĞITIK VERİ İŞLEME
# BLG462 Büyük Veri — Twitter US Airline Sentiment
# ============================================================

spark = SparkSession.builder \
    .appName('TwitterAnalysis') \
    .config("spark.sql.shuffle.partitions", "4") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

print("=" * 60)
print("SPARK OTURUMU BAŞLATILDI")
print(f"  Spark Sürümü : {spark.version}")
print("=" * 60)

# --- 4.1 Veri Yükleme ---
df_spark = spark.read.csv('tweets_temiz.csv', header=True, inferSchema=False)

# Güven sütununu sayısal yap
df_spark = df_spark.withColumn(
    'guven',
    when(col('airline_sentiment_confidence').rlike(r'^[0-9.]+$'),
         col('airline_sentiment_confidence').cast('float')).otherwise(None)
)

print("\nŞEMA:")
df_spark.printSchema()

# ============================================================
# DÖNÜŞÜMLER (Transformation) — En az 3
# ============================================================
print("\n" + "=" * 60)
print("DÖNÜŞÜMLER (Transformations)")
print("=" * 60)

# Transformation 1 — select()
print("\n[T1] select() — İlgili sütunları seçme:")
df_secili = df_spark.select(
    'tweet_id', 'airline_sentiment', 'airline', 'guven', 'text_temiz'
)
df_secili.show(5, truncate=50)

# Transformation 2 — filter() + withColumn()
print("\n[T2] filter() — Yalnızca negatif United tweetleri:")
df_negatif_united = df_spark \
    .filter((col('airline_sentiment') == 'negative') & (col('airline') == 'United')) \
    .withColumn('text_kucuk', lower(trim(col('text_temiz')))) \
    .select('airline', 'airline_sentiment', 'text_kucuk')
df_negatif_united.show(5, truncate=60)

# Transformation 3 — groupBy()
print("\n[T3] groupBy() — Havayolu ve duygu bazında tweet sayısı:")
df_grup = df_spark \
    .filter(col('airline_sentiment').isin('negative', 'neutral', 'positive')) \
    .groupBy('airline', 'airline_sentiment') \
    .count() \
    .orderBy('airline', 'count', ascending=[True, False])
df_grup.show(18)

# ============================================================
# EYLEMLER (Actions) — En az 2 (show, count, collect, describe)
# ============================================================
print("\n" + "=" * 60)
print("EYLEMLER (Actions)")
print("=" * 60)

# Action 1 — count()
toplam = df_spark.count()
print(f"\n[E1] count() — Toplam kayıt sayısı: {toplam}")

# Action 2 — describe()
print("\n[E2] describe() — Sayısal istatistikler:")
df_spark.select('guven').describe().show()

# Action 3 — collect() — ilk 3 kaydı listeye al
print("\n[E3] collect() — İlk 3 kaydı Python listesine al:")
ilk_uc = df_spark.select('airline', 'airline_sentiment', 'guven').limit(3).collect()
for satir in ilk_uc:
    print(f"  {satir}")

# Action 4 — show()
print("\n[E4] show() — Duygu dağılımı özeti:")
df_spark.filter(col('airline_sentiment').isin('negative', 'neutral', 'positive')) \
    .groupBy('airline_sentiment').count() \
    .orderBy('count', ascending=False) \
    .show()

# ============================================================
# SPARK SQL — En az 2
# ============================================================
print("\n" + "=" * 60)
print("SPARK SQL")
print("=" * 60)

df_spark.createOrReplaceTempView('tweetler')

# SQL 1 — Havayolu bazında negatif tweet sayısı
print("\n[SQL1] Havayolu bazında negatif tweet sayısı:")
spark.sql("""
    SELECT airline,
           COUNT(*) AS negatif_adet
    FROM tweetler
    WHERE airline_sentiment = 'negative'
    GROUP BY airline
    ORDER BY negatif_adet DESC
""").show()

# SQL 2 — Güven skoru > 0.9 olan duygu dağılımı
print("\n[SQL2] Güven skoru 0.9 üzeri tweetlerin duygu dağılımı:")
spark.sql("""
    SELECT airline_sentiment,
           COUNT(*) AS adet,
           ROUND(AVG(CAST(guven AS FLOAT)), 3) AS ort_guven
    FROM tweetler
    WHERE guven > 0.9
    GROUP BY airline_sentiment
    ORDER BY adet DESC
""").show()

# ============================================================
# PANDAS vs PYSPARK KARŞILAŞTIRMASI
# ============================================================
print("\n" + "=" * 60)
print("PANDAS vs PYSPARK SÜRE KARŞILAŞTIRMASI")
print("=" * 60)

# Pandas
t1 = time.time()
df_pd = pd.read_csv('tweets_temiz.csv')
_ = df_pd.groupby('airline_sentiment').size()
t2 = time.time()
pandas_sure = round(t2 - t1, 4)

# PySpark
t3 = time.time()
df_spark.groupBy('airline_sentiment').count().collect()
t4 = time.time()
pyspark_sure = round(t4 - t3, 4)

print(f"\n  Pandas  süresi : {pandas_sure} saniye")
print(f"  PySpark süresi : {pyspark_sure} saniye")
print(f"""
  YORUM:
  Küçük veri setlerinde (~14.000 kayıt) Pandas genellikle daha hızlıdır,
  çünkü PySpark'ın başlatma ve görev planlama maliyeti vardır.
  Milyonlarca kayıtta PySpark çok çekirdekli dağıtık işleme ile Pandas'ı geçer.
""")

print("=" * 60)
print("✓ PySpark aşaması tamamlandı.")
print("=" * 60)

spark.stop()
