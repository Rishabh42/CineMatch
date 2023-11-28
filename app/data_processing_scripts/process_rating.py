import os
import subprocess
import time

# Set BASE_DIR to the root directory of your app
BASE_DIR = '/home/team-4/app'
DATA_COLLECTION_DIR = os.path.join(BASE_DIR, 'dummy_data_test')
DATA_COLLECTION_PATH = os.path.join(DATA_COLLECTION_DIR, 'ratings.csv')
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'cleaned_rating.csv')  # Processed file path
TARGET_FILE_PATH = os.path.join(BASE_DIR, 'data', 'cleaned_rating.csv')  # Final file path

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def run_kafka_consumer(duration_in_minutes):
    ensure_directory_exists(DATA_COLLECTION_DIR)

def process_ratings():
    processing_script_path = os.path.join(BASE_DIR, "data_processing_scripts", "process_rating.py")
    subprocess.run(['python3', processing_script_path, DATA_COLLECTION_PATH], check=True)

def append_to_cleaned_data():
    if not os.path.isfile(PROCESSED_DATA_PATH):
        print(f"Processed file {PROCESSED_DATA_PATH} does not exist.")
        return

    skip_header = os.path.isfile(TARGET_FILE_PATH) and os.path.getsize(TARGET_FILE_PATH) > 0

    with open(PROCESSED_DATA_PATH, 'r') as infile:
        lines = infile.readlines()

    with open(TARGET_FILE_PATH, 'a') as outfile:
        if skip_header:
            lines = lines[1:]  
        outfile.writelines(lines)

def main():
    run_kafka_consumer(1)
    process_ratings()
    append_to_cleaned_data()
    if os.path.exists(PROCESSED_DATA_PATH):
        os.remove(PROCESSED_DATA_PATH)

if __name__ == "__main__":
    main()
