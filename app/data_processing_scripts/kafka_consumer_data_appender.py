import os
import subprocess
import time

# This should be the root directory of your app, adjust accordingly.
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_COLLECTION_DIR = os.path.join(BASE_DIR, 'dummy_data_test')
DATA_COLLECTION_PATH = os.path.join(DATA_COLLECTION_DIR, 'ratings.csv')
CLEANED_DATA_PATH = os.path.join(BASE_DIR, 'cleaned_rating.csv')
TARGET_FILE_PATH = os.path.join(BASE_DIR, 'data', 'cleaned_rating.csv')

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def run_kafka_consumer(duration_in_minutes):
    ensure_directory_exists(DATA_COLLECTION_DIR)

    kafka_command = (
        "docker run --log-opt max-size=50m --log-opt max-file=5 "
        "bitnami/kafka kafka-console-consumer.sh "
        "--bootstrap-server fall2023-comp585.cs.mcgill.ca:9092 "
        "--topic movielog4"
    )
    
    process = subprocess.Popen(kafka_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    start_time = time.time()
    output = []

    try:
        while time.time() - start_time <= duration_in_minutes * 60:
            line = process.stdout.readline()
            if line:
                output.append(line.decode('utf-8').strip())
    finally:
        process.kill()

    with open(DATA_COLLECTION_PATH, 'w') as file:
        file.writelines(line + '\n' for line in output)

def run_processing_script():
    processing_command = f'python3 {os.path.join(BASE_DIR, "data_processing_scripts", "process_rating.py")} {DATA_COLLECTION_PATH}'
    os.system(processing_command)

def append_to_cleaned_data():
    if not os.path.isfile(CLEANED_DATA_PATH):
        print(f"Processed file {CLEANED_DATA_PATH} does not exist.")
        return

    with open(CLEANED_DATA_PATH, 'r') as infile, open(TARGET_FILE_PATH, 'a') as outfile:
        next(infile)  # Skip the header
        outfile.writelines(infile.readlines())

def main():
    run_kafka_consumer(1)
    run_processing_script()
    append_to_cleaned_data()
    os.remove(CLEANED_DATA_PATH)

if __name__ == "__main__":
    main()
