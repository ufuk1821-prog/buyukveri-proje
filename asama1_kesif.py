import pandas as pd

df = pd.read_csv('Tweets.csv', encoding='latin-1')

print(df.shape)
print(df.columns.tolist())
print(df.dtypes)
print(df.head(3))
print(df.describe())
print(df.info())