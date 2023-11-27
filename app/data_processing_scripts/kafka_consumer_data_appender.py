import subprocess
import time
import os

def run_kafka_consumer(duration_in_minutes):

    kafka_command = ("docker run -it --log-opt max-size=50m --log-opt max-file=5 "
                     "bitnami/kafka kafka-console-consumer.sh "
                     "--bootstrap-server fall2023-comp585.cs.mcgill.ca:9092 "
                     "--topic movielog4")

    # Run the command and collect data for the specified duration
    start_time = time.time()
    process = subprocess.Popen(kafka_command, shell=True, stdout=subprocess.PIPE)

    while True:
        if time.time() - start_time > duration_in_minutes * 60:
            process.terminate()
            break

    output, _ = process.communicate()
    with open('kafka_output.txt', 'wb') as file:
        file.write(output)

# def run_processing_script():
#     os.system('/app/data_processing_scripts/process_rating.py kafka_output.txt')

# def append_to_cleaned_data():
#     with open('/app/data/cleaned_rating.csv', 'a') as outfile, open('cleaned_rating.csv', 'r') as infile:
#         outfile.write(infile.read())

def main():
    # Run Kafka Consumer for 15 minutes
    run_kafka_consumer(15)

    time.sleep(300)

    run_processing_script()

    append_to_cleaned_data()

    os.remove('cleaned_rating.csv')

if __name__ == "__main__":
    main()
