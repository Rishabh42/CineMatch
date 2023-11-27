import subprocess
import time
import os

DATA_COLLECTION_PATH = 'dummy_data_test/ratings.csv'
CLEANED_DATA_PATH = 'cleaned_rating.csv'
TARGET_FILE_PATH = '/app/data/cleaned_rating.csv'

def run_kafka_consumer(duration_in_minutes):
    kafka_command = ("docker run -it --log-opt max-size=50m --log-opt max-file=5 "
                     "bitnami/kafka kafka-console-consumer.sh "
                     "--bootstrap-server fall2023-comp585.cs.mcgill.ca:9092 "
                     "--topic movielog4")
    
    start_time = time.time()
    process = subprocess.Popen(kafka_command, shell=True, stdout=subprocess.PIPE)

    while True:
        if time.time() - start_time > duration_in_minutes * 60:
            process.terminate()
            break

    output, _ = process.communicate()
    with open(DATA_COLLECTION_PATH, 'wb') as file:
        file.write(output)

def run_processing_script():
    os.system('/app/data_processing_scripts/process_rating.py')

def append_to_cleaned_data():
    with open(TARGET_FILE_PATH, 'a') as outfile, open(CLEANED_DATA_PATH, 'r') as infile:
        next(infile)  
        outfile.write(infile.read())

def main():
    run_kafka_consumer(15)
    time.sleep(300)  
    run_processing_script()
    append_to_cleaned_data()

    os.remove(CLEANED_DATA_PATH)

if __name__ == "__main__":
    main()
