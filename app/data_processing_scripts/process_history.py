import pandas as pd
import re
from dateutil import parser

# Load data
df = pd.read_csv('history1.csv', names=['raw'], sep='\t')
# Split the data
df_split = df['raw'].str.split(',', expand=True)
df_split.columns = ['time', 'userid', 'data']

# Extract movie name and minute from the data column
pattern = r'GET /data/m/(.*?)/(\d+)\.mpg'
df_split[['movieid', 'minute']] = df_split['data'].str.extract(pattern)
df_split.drop(columns=['data', 'time'], inplace=True)
df_split = df_split.iloc[::-1]
df_split.drop_duplicates(subset=['userid', 'movieid'], inplace=True)

# Write to CSV
df_split.to_csv('cleaned_history.csv', index=False)

print(df_split.head())
