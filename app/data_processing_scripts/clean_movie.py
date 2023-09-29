import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('movie_cleaned_1.csv')

# Remove rows with duplicate entries in all columns
df = df.drop_duplicates(subset=["movieid"])

# Save the updated DataFrame to a new CSV file
df.to_csv('final_cleaned_movie_list.csv', index=False)