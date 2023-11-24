#!/bin/bash

# Build the canary version of the application
cd ~/app
git checkout main 
cd app 
docker compose up -d --build --force-recreate inference_canary

# Sleep for 12 hours
sleep $((12 * 60 * 60))

threshold=500
# Calculate averag response time over the last 12 hours
avg_response_time=$(curl -g 'http://prometheus-server:9090/api/v1/query' --data-urlencode 'query=sum(flask_http_request_duration_seconds_sum) / sum(flask_http_request_duration_seconds_count)' | jq -r '.data.result[0].value[1]')

echo "Average response time over the last 12 hours: $avg_response_time"

if (( $(echo "$avg_response_time < $threshold" | bc -l) )); then
  echo "Switching from canary to stable deployment..."
  docker compose up -d --build --force-recreate inference_stable
else
  echo "Average response time is greater than threshold ($avg_response_time ms > 500 ms). Canary release aborted."
fi

docker stop canary-controller 
docker rm canary-controller
