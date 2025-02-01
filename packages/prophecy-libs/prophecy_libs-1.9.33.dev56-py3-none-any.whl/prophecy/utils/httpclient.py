import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import gzip
import json
from .datasampleloader import DataSampleLoader

class HTTPClientError(Exception):
    """Custom exception for HTTP client errors"""
    pass

class HttpClient:
    def __init__(self):
        self.session = self._create_session()

    @staticmethod
    def _create_session() -> requests.Session:
        session = requests.Session()

        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )

        # Configure the adapter with retry strategy and pooling
        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=5,
            pool_block=True
        )

        # Mount the adapter for both HTTP and HTTPS
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set default headers
        session.headers.update({
            'Accept': 'application/json',
            'Authorization': f'Bearer {ProphecyConstants.TOKEN}'
        })

        # Set default timeout for all requests
        session.timeout = (10, 30)  # (connect timeout, read timeout)

        return session

    @classmethod
    def _handle_response(cls, response: requests.Response) -> str:
        """Handle the HTTP response and return the response body"""
        try:
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            raise HTTPClientError(f"HTTP Request failed: {str(e)}") from e

    @classmethod
    def _build_url(cls, endpoint: str) -> str:
        """Build the full URL from the endpoint"""
        return f"{ProphecyConstants.BASE_URL.rstrip('/')}/{endpoint.lstrip('/')}"

    @classmethod
    def get(cls, endpoint: str) -> str:
        """
        Execute a GET request
        Args:
            endpoint: The API endpoint to call
        Returns:
            The response body as a string
        Raises:
            HTTPClientError: If the request fails
        """
        try:
            with cls() as client:
                response = client.session.get(
                    cls._build_url(endpoint)
                )
                return cls._handle_response(response)
        except Exception as e:
            raise HTTPClientError(f"GET request failed: {str(e)}") from e

    @classmethod
    def post(cls, endpoint: str, body: str) -> str:
        """
        Execute a POST request
        Args:
            endpoint: The API endpoint to call
            body: The request body as a string
        Returns:
            The response body as a string
        Raises:
            HTTPClientError: If the request fails
        """
        try:
            with cls() as client:
                response = client.session.post(
                    cls._build_url(endpoint),
                    data=body,
                    headers={'Content-Type': 'application/json'}
                )
                return cls._handle_response(response)
        except Exception as e:
            raise HTTPClientError(f"POST request failed: {str(e)}") from e

    @classmethod
    def post_compressed(cls, endpoint: str, body: str) -> str:
        """
        Execute a POST request with gzipped body
        Args:
            endpoint: The API endpoint to call
            body: The request body as a string
        Returns:
            The response body as a string
        Raises:
            HTTPClientError: If the request fails
        """
        try:
            compressed_data = gzip.compress(body.encode('utf-8'))

            with cls() as client:
                response = client.session.post(
                    cls._build_url(endpoint),
                    data=compressed_data,
                    headers={
                        'Content-Type': 'application/json',
                        'Content-Encoding': 'gzip'
                    }
                )
                return cls._handle_response(response)
        except Exception as e:
            raise HTTPClientError(f"Compressed POST request failed: {str(e)}") from e

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - ensures session is closed"""
        self.session.close()


class ProphecyRequests:
    @staticmethod
    def ping():
        try:
            print(f"Prophecy Base URL: {ProphecyConstants.BASE_URL}")
            response = HttpClient.get("/ping")
            print(f"Ping Response: {response}")
        except HTTPClientError as e:
            print(f"Ping Request Failed: {str(e)}")

    @staticmethod
    def send_dataframe_payload(key: str, job: str, df_offset: int = 0):
        try:
            payload = DataSampleLoader.get_payload(key, job, df_offset)
            response = HttpClient.post_compressed("/interims", payload)
            print(f"Interims Response: {response}")
        except HTTPClientError as e:
            print(f"Interims Request Failed HTTPClientError: {str(e)}")
        except Exception as e:
            print(f"Interims Request Failed: {str(e)}")

ProphecyRequests.ping()