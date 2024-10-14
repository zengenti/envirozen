import requests
import logging
from config import PROMETHEUS_URL

# Configure logging (You can configure this in the main file if it's a bigger project)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def query_prometheus(query):
    """
    Queries the Prometheus API for the given query.

    Parameters:
    - query (str): The Prometheus query string to be executed.

    Returns:
    - list: The results of the query if successful.

    Raises:
    - ValueError: If the query is invalid (empty or None).
    - Exception: If the query fails or returns an error.
    """
    # Validate the query
    if not query:
        logging.error("The Prometheus query is empty or None.")
        raise ValueError("Prometheus query cannot be empty or None.")

    try:
        # Log the query being sent
        logging.info(f"Sending Prometheus query: {query}")

        # Send a GET request to the Prometheus query API
        response = requests.get(f'{PROMETHEUS_URL}/api/v1/query', params={'query': query})

        # Log the response status code
        logging.info(f"Prometheus query response status: {response.status_code}")

        # Raise an error for bad responses (4xx and 5xx status codes)
        response.raise_for_status()

        # Parse the JSON response
        data = response.json()

        # Check if the query was successful
        if data['status'] != 'success':
            logging.error(f"Prometheus query failed with error: {data.get('error', 'Unknown error')}")
            logging.error(f"Prometheus full response: {data}")
            raise Exception(f"Failed to query Prometheus: {data.get('error', 'Unknown error')}")

        # Log successful query result
        logging.info(f"Prometheus query successful, results count: {len(data['data']['result'])}")
        return data['data']['result']

    except requests.exceptions.RequestException as e:
        # Log the exception related to the request
        logging.error(f"Request to Prometheus failed: {str(e)}")
        raise Exception(f"Request to Prometheus failed: {str(e)}")
