#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ./m365_user_manager/managers/token_manager.py

from typing import Optional
from logging import Logger
import aiohttp
import asyncio
import time
from cw_rpa import HttpClient
from m365_user_manager.exceptions.exceptions import TokenManagerError

class TokenManager:
    def __init__(self, discord_webhook_url: str = None, logger: Optional[Logger] = None):
        self.discord_webhook_url = discord_webhook_url
        self.logger = logger
        self._access_tokens = {}  # Dictionary to store tokens based on scope
        self._token_expiry = {}   # Dictionary to store token expiry times
        self.http_client = HttpClient()  # Assuming this is an async-compatible HttpClient

    async def _fetch_token(self, token_url: str, token_data: dict, scope_key: str) -> Optional[str]:
        """
        Internal method to fetch access tokens asynchronously.

        Args:
            token_url (str): The token endpoint URL.
            token_data (dict): The data payload for the token request.
            scope_key (str): A unique key representing the scope for caching.

        Returns:
            Optional[str]: The access token if successful, else None.

        Raises:
            TokenManagerError: If token acquisition fails.
        """
        current_time = time.time()
        # Check if token is cached and valid
        if scope_key in self._access_tokens and current_time < self._token_expiry.get(scope_key, 0):
            return self._access_tokens[scope_key]

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(token_url, data=token_data, timeout=30) as response:
                    if response.status == 401:
                        raise TokenManagerError(
                            "Invalid authentication credentials provided",
                            status_code=401
                        )
                    response.raise_for_status()
                    token_response = await response.json()

                    if "access_token" not in token_response:
                        raise TokenManagerError(
                            "Invalid response: No access token returned",
                            status_code=response.status
                        )

                    access_token = token_response["access_token"]
                    expires_in = token_response.get("expires_in", 3600)  # Default to 1 hour
                    self._access_tokens[scope_key] = access_token
                    self._token_expiry[scope_key] = current_time + expires_in - 300  # Refresh 5 minutes before expiry
                    return access_token

            except asyncio.TimeoutError:
                self.logger.error("Token request timed out after 30 seconds")
                raise TokenManagerError(
                    "Token request timed out after 30 seconds",
                    status_code=408
                )
            except aiohttp.ClientResponseError as e:
                self.logger.error(f"Failed to acquire access token: {str(e)}")
                raise TokenManagerError(
                    f"Token acquisition failed: {str(e)}",
                    status_code=e.status
                )
            except aiohttp.ClientError as e:
                self.logger.error(f"Failed to acquire access token: {str(e)}")
                raise TokenManagerError(
                    f"Token acquisition failed: {str(e)}",
                    status_code=500
                )
            except Exception as e:
                self.logger.error(f"Failed to acquire access token: {str(e)}")
                raise TokenManagerError(
                    f"Token acquisition failed: {str(e)}",
                    status_code=500
                )

    async def get_access_token(self, client_id: str, client_secret: str, tenant_id: str) -> str:
        """
        Get Microsoft Graph API access token with required permissions.

        Args:
            client_id (str): Azure AD application client ID.
            client_secret (str): Azure AD application client secret.
            tenant_id (str): Azure AD tenant ID.

        Returns:
            str: Microsoft Graph API access token.

        Raises:
            TokenManagerError: If token acquisition fails.
        """
        token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
        token_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "https://graph.microsoft.com/.default"
        }
        scope_key = "graph_api"

        token = await self._fetch_token(token_url, token_data, scope_key)
        return token

    async def get_asio_token(self, client_id: str, client_secret: str) -> str:
        """
        Get Asio access token with required permissions.

        Args:
            client_id (str): Azure AD application client ID.
            client_secret (str): Azure AD application client secret.

        Returns:
            str: Asio access token.

        Raises:
            TokenManagerError: If token acquisition fails.
        """
        token_url = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
        token_data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": "platform.rpa.resolve"
        }
        scope_key = "platform_rpa_resolve"

        token = await self._fetch_token(token_url, token_data, scope_key)
        return token
