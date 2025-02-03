# fetch_html.py
# author: Lixuan Lin
# date: 2025-01-16

import requests
from requests.exceptions import RequestException

def fetch_html(url, timeout=10):
    """
    Fetches the HTML content of a given URL.

    Parameters:
        url (str): The URL of the webpage to fetch.
        timeout (int, optional): The maximum time to wait for a response, in seconds. Defaults to 10 seconds.

    Returns:
        str: The raw HTML content of the webpage if the request is successful.

    Raises:
        ValueError: If the URL provided is invalid or improperly formatted.
        requests.exceptions.Timeout: If the request times out before receiving a response.
        requests.exceptions.RequestException: For other issues during the HTTP request, such as connectivity problems
            or a non-success HTTP status code.

    Examples:
        Fetch the HTML content of a webpage:
        >>> html_content = fetch_html("https://example.com")
        >>> print(html_content[:100])  # Prints the first 100 characters of the HTML content

    Notes:
        - This function uses the `requests` library to perform an HTTP GET request.
        - Ensure the `requests` library is installed before using this function.
    """
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        return response.text
    except requests.exceptions.Timeout:
        raise 
    except RequestException as e:
        raise ValueError(f"Failed to fetch HTML from {url}: {e}")
