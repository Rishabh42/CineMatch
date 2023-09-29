import pandas as pd
import re
from dateutil import parser

# Load data
df = pd.read_csv('output.csv', names=['raw'], sep='\t')  
# Split the data
df_split = df['raw'].str.split(',', expand=True)
df_split.columns = ['time', 'userid', 'data']

# Extract movie name and minute from the data column
pattern = r'GET /data/m/(.*?)/(\d+)\.mpg'
df_split[['movieid', 'minute']] = df_split['data'].str.extract(pattern)
df_split.drop(columns=['data'], inplace=True)

def try_parse(date_str):
    try:
        return parser.parse(date_str)
    except:
        return pd.NaT

df_split['time'] = df_split['time'].apply(try_parse)
df_split = df_split.dropna(subset=['time'])  # remove rows with NaT in 'time' column

# Write to CSV
df_split.to_csv('final_cleaned_output.csv', index=False)

print(df_split.head())

