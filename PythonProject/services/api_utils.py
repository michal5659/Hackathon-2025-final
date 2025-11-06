from typing import Optional, Dict, Any
import requests


class ApiUtils:

    def get_api(self, url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Generic GET method to call any API endpoint.

        Args:
            url: The complete URL for the GET request.
            headers: Optional dictionary containing HTTP headers. If None, uses default headers.

        Returns:
            Dictionary containing the API response.

        Raises:
            requests.exceptions.RequestException: If the API call fails.
        """
        print("Inside get_api method")
        default_headers = {
            'accept': 'application/json',
            'userName': 'Administrator',
            'password': '1111'
        }

        request_headers = headers or default_headers

        try:
            print(f"Sending GET request to: {url}")
            print(f"Headers: {request_headers}")
            response = requests.get(url, headers=request_headers)
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling GET API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response text: {e.response.text}")
            raise

    def post_api(self, url: str, json_data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Generic POST method to call any API endpoint.

        Args:
            url: The complete URL for the POST request.
            json_data: Dictionary containing the JSON data to send in the request body.
            headers: Optional dictionary containing HTTP headers. If None, uses default headers.

        Returns:
            Dictionary containing the API response.

        Raises:
            requests.exceptions.RequestException: If the API call fails.
        """
        default_headers = {
            'accept': 'application/json',
            'userName': 'Administrator',
            'password': '1111',
            'Content-Type': 'application/json'
        }

        request_headers = headers or default_headers

        try:
            print(f"Sending POST request to: {url}")
            print(f"Headers: {request_headers}")
            print(f"Body: {json_data}")
            response = requests.post(url, headers=request_headers, json=json_data)
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling POST API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response text: {e.response.text}")
            raise

    def put_api(self, url: str, json_data: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Generic PUT method to call any API endpoint.

        Args:
            url: The complete URL for the PUT request.
            json_data: Dictionary containing the JSON data to send in the request body.
            headers: Optional dictionary containing HTTP headers. If None, uses default headers.

        Returns:
            Dictionary containing the API response.

        Raises:
            requests.exceptions.RequestException: If the API call fails.
        """
        default_headers = {
            'accept': 'application/json',
            'userName': 'Administrator',
            'password': '1111',
            'Content-Type': 'application/json'
        }

        request_headers = headers or default_headers

        try:
            print(f"Sending PUT request to: {url}")
            print(f"Headers: {request_headers}")
            print(f"Body: {json_data}")
            response = requests.put(url, headers=request_headers, json=json_data)
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error calling PUT API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response text: {e.response.text}")

    pass


# Singleton instance
_api_utils = None


def get_api_utils() -> ApiUtils:
    """Get or create task execution agent singleton"""
    global _api_utils
    if _api_utils is None:
        _api_utils = ApiUtils()
    return _api_utils

 