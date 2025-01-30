import requests
from cw_rpa import HttpClient
from typing import Any, Dict, Optional
from logging import Logger

from m365_user_manager.exceptions.exceptions import (
    GraphAPIError, 
    InsufficientPermissionsError
)

class RequestManager:
    def __init__(self, access_token: str, graph_endpoint: str, 
                 running_in_asio: bool = False,
                 http_client: Optional[HttpClient] = None,
                 max_retries: int = 3,
                 timeout: int = 30,
                 logger: Optional[Logger] = None):
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        self.graph_endpoint = graph_endpoint
        self.running_in_asio = running_in_asio
        self.http_client = http_client
        self.max_retries = max_retries
        self.timeout = timeout
        self.logger = logger
        
        # Add immediate logging test
        self.logger.debug("RequestManager initialized")

    async def make_request(self, method: str, endpoint: str,
                         json_data: Optional[Dict] = None,
                         params: Optional[Dict] = None,
                         retry_count: int = 0) -> requests.Response:
        """Make API request with retry logic and error handling."""
        url = f"{self.graph_endpoint}/{endpoint}"
        
        try:
            if self.running_in_asio:
                print("Running in Asio environment")
                integration_client = self.http_client.third_party_integration("azure_o365")
                response = await self._make_asio_request(
                    integration_client, method, url, json_data, params
                )
            else:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=self.headers,
                    json=json_data,
                    params=params,
                    timeout=self.timeout
                )

            if response.status_code == 403:
                raise InsufficientPermissionsError(
                    "Insufficient permissions for this operation",
                    required_permissions=['Directory.ReadWrite.All']
                )

            response.raise_for_status()
            return response

        except requests.exceptions.RequestException as e:
            if retry_count < self.max_retries and self._should_retry(e):
                self.logger.warning(
                    f"Request failed, attempt {retry_count + 1} of {self.max_retries}"
                )
                return await self.make_request(
                    method, endpoint, json_data, params, retry_count + 1
                )
            raise GraphAPIError(str(e), status_code=getattr(e, 'response', {}).status_code or 500)

    def _should_retry(self, error: Exception) -> bool:
        """Determine if request should be retried based on error."""
        if isinstance(error, requests.exceptions.Timeout):
            return True
        if hasattr(error, 'response'):
            return error.response.status_code >= 500
        return False

    async def _make_asio_request(self, client: Any, method: str, 
                                url: str, json_data: Optional[Dict], 
                                params: Optional[Dict]) -> Any:
        """Make request using Asio HTTP client."""
        if method.upper() == "GET":
            return await client.get(url=url, headers=self.headers, params=params)
        elif method.upper() == "POST":
            return await client.post(url=url, headers=self.headers, json=json_data)
        elif method.upper() == "PATCH":
            return await client.patch(url=url, headers=self.headers, json=json_data)
        raise GraphAPIError(f"Unsupported HTTP method: {method}", status_code=400)
