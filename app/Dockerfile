# Pull alpine library of Python for better resource utilization
FROM python:3.9.18

# Set working directory as app
WORKDIR /app

# Install required libraries
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the files from our application
ADD app.py app.py
COPY model/ model/
COPY data/ data/

# Expose port 8082 from the container
EXPOSE 8082

# Start the Python application
CMD ["gunicorn", "--bind", "0.0.0.0:8082", "app:app"]

# to run
# docker build -t service .
# docker compose up -d
# docker exec -it recommender /bin/bash
