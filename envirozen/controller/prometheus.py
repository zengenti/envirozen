import requests
from config import PROMETHEUS_URL

def query_prometheus(query):
    """
    Queries the Prometheus API for the given query.

    Parameters:
    - query (str): The Prometheus query string to be executed.

    Returns:
    - list: The results of the query if successful.

    Raises:
    - Exception: If the query fails or returns an error.
    """
    try:
        # Send a GET request to the Prometheus query API
        response = requests.get(f'{PROMETHEUS_URL}/api/v1/query', params={'query': query})

        # Raise an error for bad responses (4xx and 5xx status codes)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Check if the query was successful
        if data['status'] == 'success':
            return data['data']['result']
        else:
            raise Exception(f"Failed to query Prometheus: {data.get('error', 'Unknown error')}")

    except requests.exceptions.RequestException as e:
        # Handle any requests-related exceptions (e.g., network issues)
        raise Exception(f"Request to Prometheus failed: {str(e)}")
