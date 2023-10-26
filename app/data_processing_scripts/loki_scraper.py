import requests
import urllib.parse


def fetch_logs_latest(type):
    """
    Fetches logs of a given type from a remote server.

    :param type (str): The type of logs to fetch. Value can be history, rating or error
    :return (str): a list of the 100 latest logs from the Kafka stream at the time of calling the API. each array item is in the following format based on type
                   history: (timestamp, userid, movieid, minute of movie watched)
                   rating: (timestamp, userid, movieid, rating)
                   error: (timestamp, userid, error, message, response time)
    """
    data = {'query': '{type="' + type + '"}'}
    encoded_data = urllib.parse.urlencode(data)
    res = requests.get(
        "http://fall2023-comp585-4.cs.mcgill.ca:3100/loki/api/v1/query?" + encoded_data)

    return res.json()['data']['result'][0]['values']


print(fetch_logs_latest('history'))
