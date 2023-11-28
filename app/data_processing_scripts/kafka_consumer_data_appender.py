import subprocess
import time
import os

DATA_COLLECTION_PATH = 'dummy_data_test/ratings.csv'
CLEANED_DATA_PATH = 'cleaned_rating.csv'
TARGET_FILE_PATH = '/home/team-4/app/data/cleaned_rating.csv'

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def run_kafka_consumer(duration_in_minutes):
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

    ensure_directory_exists(os.path.dirname(DATA_COLLECTION_PATH))
    with open(DATA_COLLECTION_PATH, 'w') as file:
        for line in output:
            file.write(line + '\n')

def run_processing_script():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    process_script_path = os.path.join(script_dir, 'process_rating.py')
    os.system(f'python3 {process_script_path}')

def append_to_cleaned_data():
    ensure_directory_exists(os.path.dirname(TARGET_FILE_PATH))
    if not os.path.exists(TARGET_FILE_PATH):
        open(TARGET_FILE_PATH, 'a').close()

    with open(TARGET_FILE_PATH, 'a') as outfile, open(CLEANED_DATA_PATH, 'r') as infile:
        next(infile)  # Skip the header
        outfile.write(infile.read())

def main():
    run_kafka_consumer(1)
    run_processing_script()
    append_to_cleaned_data()

if __name__ == "__main__":
    main()
