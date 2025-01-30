#!/usr/bin/env python
# -*- coding: utf-8 -*-

from m365_user_manager import UserManagementOrchestrator, FormFields
import asyncio
import logging
import argparse
from logging import Logger
from typing import Optional
from m365_user_manager.exceptions.exceptions import TokenManagerError
import requests
from cw_rpa import Logger, HttpClient, Input
import json
import os

def get_access_token(log: Logger) -> Optional[str]:
    """
    Fetch access token from the integration client.
    Returns the token if successful, None otherwise.
    """
    http_client = HttpClient()
    integration_name = "azure_o365"
    integration_client = http_client.third_party_integration(integration_name)
    try:
        token_response = integration_client.fetch_token(
            client_id=integration_client.client_id,
            client_secret=integration_client.client_secret,
            scopes=["platform.rpa.resolve"]
        )

        if not token_response or not token_response.token:
            log.critical(
                f"Failed to fetch token, status code: {token_response.status_code}, response: {token_response.text}"
            )
            log.result_failed_message("Token fetch failed.")
            return None

        return token_response.token

    except Exception as e:
        log.exception(e, "Failed to fetch access token.")
        return None

def graph_access_token(client_id: str, client_secret: str, tenant_id: str) -> str:
    logger = logging.getLogger(__name__)
    if not all([client_id, client_secret, tenant_id]):
        missing = []
        if not client_id: missing.append("client_id")
        if not client_secret: missing.append("client_secret")
        if not tenant_id: missing.append("tenant_id")
        raise TokenManagerError(
            f"Missing required credentials: {', '.join(missing)}",
            status_code=400
        )
        
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    token_data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default"
    }
    
    try:
        response = requests.post(token_url, data=token_data, timeout=30)
        response.raise_for_status()
        token_data = response.json()
        
        if "access_token" not in token_data:
            raise TokenManagerError(
                "Invalid response: No access token returned",
                status_code=response.status_code
            )
            
        return token_data["access_token"]
        
    except requests.exceptions.RequestException as e:
        error_msg = f"Token acquisition failed: {str(e)}"
        logger.error(error_msg)
        raise TokenManagerError(error_msg, 
            status_code=getattr(e.response, 'status_code', 500)
        )

async def main():
    try:
        # Initialize Input handling first
        input_obj = Input()
        input_obj.load_data()  # This will try args first, then fall back to file
        
        # Determine if running in ASIO
        RUNNING_IN_ASIO = False
        access_token = None

        # Handle access token based on environment
        if not RUNNING_IN_ASIO:
            # Parse config file path
            config_path = "m365_user_manager/environments/asio_365_config.json"

            # Load configuration and get token
            with open(config_path, 'r') as f:
                config = json.load(f)
                print(f"Loaded config: {config}")
            
            access_token = graph_access_token(
                client_id=config["client_id"],
                client_secret=config["client_secret"],
                tenant_id=config["tenant_id"]
            )
        else:
            # ASIO environment handling
            temp_logger = Logger()
            access_token = get_access_token(temp_logger)
            if not access_token:
                raise Exception("Failed to obtain access token in ASIO environment")

        # Create and initialize orchestrator
        try:
            orchestrator = await UserManagementOrchestrator.create(
                log_level=logging.DEBUG, 
                access_token=access_token
            )
        except Exception as e:
            print(f"Failed to create orchestrator: {e}")
            raise
            
        # Run main process
        await orchestrator.run()
        
    except Exception as e:
        print(f"Critical error in main: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())