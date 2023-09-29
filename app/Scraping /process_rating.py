import pandas as pd
import re

def determine_format(dt_str):
    try:
        pd.to_datetime(dt_str, format="%Y-%m-%dT%H:%M:%S")
        return "%Y-%m-%dT%H:%M:%S"
    except:
        try:
            pd.to_datetime(dt_str, format="%Y-%m-%dT%H:%M")
            return "%Y-%m-%dT%H:%M"
        except:
            return None

# Load data
df = pd.read_csv('rating.csv', names=['raw'], sep='\t')

# Splitting the raw data into separate columns
df_split = df['raw'].str.split(',', expand=True)
df_split.columns = ['time', 'userid', 'data']

# Extract movie name and rating from the data column
pattern = r'GET /rate/(.*?)=(\d)'
df_split[['movieid', 'rating']] = df_split['data'].str.extract(pattern)
df_split.drop(columns=['data'], inplace=True)
df_split['time'] = df_split['time'].apply(lambda x: pd.to_datetime(x, format=determine_format(x), errors='coerce'))
df_split.to_csv('cleaned_rating.csv', index=False)

print(df_split.head())

