import csv

# Open the CSV file for reading
with open('movie_list.csv', 'r') as csvfile:
    # Create a CSV reader
    csvreader = csv.reader(csvfile)
    
    # Skip the header row if it exists
    next(csvreader, None)
    
    # Loop through each row in the CSV file
    for row in csvreader:
        # The 'movieid' column is at index 1 (0-based indexing)
        movie_id = row[1]
        
        # You can perform any operations you want on movie_id here
        print(movie_id)  # For example, print the movie_id

# Close the CSV file
csvfile.close()
