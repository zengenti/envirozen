
import requests
from config import PROMETHEUS_URL

def query_prometheus(query):
    response = requests.get(f'{PROMETHEUS_URL}/api/v1/query', params={'query': query})
    data = response.json()
    if data['status'] == 'success':
        return data['data']['result']
    else:
        raise Exception(f"Failed to query Prometheus: {data['error']}")
