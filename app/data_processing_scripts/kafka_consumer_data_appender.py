import subprocess
import os
import time

BASE_DIR = os.path.dirname(__file__)
DATA_COLLECTION_DIR = os.path.join(BASE_DIR, 'dummy_data_test')
DATA_COLLECTION_PATH = os.path.join(DATA_COLLECTION_DIR, 'ratings.csv')
CLEANED_DATA_PATH = os.path.join(BASE_DIR, 'cleaned_rating.csv')
TARGET_FILE_PATH = os.path.join('/app/data', 'cleaned_rating.csv')

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def run_kafka_consumer(duration_in_minutes):
    ensure_directory_exists(DATA_COLLECTION_DIR)

    kafka_command = ("docker run --log-opt max-size=50m --log-opt max-file=5 "
                     "bitnami/kafka kafka-console-consumer.sh "
                     "--bootstrap-server fall2023-comp585.cs.mcgill.ca:9092 "
                     "--topic movielog4")

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
    os.system(f'python /app/data_processing_scripts/process_rating.py {DATA_COLLECTION_PATH}')

def append_to_cleaned_data():
    with open(CLEANED_DATA_PATH, 'r') as infile:
        lines = infile.readlines()

    with open(TARGET_FILE_PATH, 'a') as outfile:
        if os.path.getsize(TARGET_FILE_PATH) > 0:  #
            lines = lines[1:]  
        outfile.writelines(lines)

def main():
    run_kafka_consumer(1)
    time.sleep(300)  # Optional: sleep for a bit
    run_processing_script()
    append_to_cleaned_data()
    os.remove(CLEANED_DATA_PATH)

if __name__ == "__main__":
    main()
