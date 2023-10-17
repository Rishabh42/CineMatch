import requests
import math
import random

for i in range(10):
    url = f"http://127.0.0.1:8082/recommend/{math.floor(random.random()*1000000)}"
    response = requests.get(url)

    print("Response code and time:", response.status_code,
          (response.elapsed.total_seconds()*1000), "milliseconds")
