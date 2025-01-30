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
from cw_rpa import Logger

main_logger = Logger()

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
    logger = main_logger
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
        main_logger.info("Input object initialized")
        main_logger.info(getattr(input_obj, '_data', None))
        
        # Determine if running in ASIO
        RUNNING_IN_ASIO = False
        access_token = None

        # Handle access token based on environment
        if not RUNNING_IN_ASIO:
            # Parse config file path
            main_logger.info("Running in local environment")
            config_path = "m365_user_manager/environments/asio_365_config.json"

            # Load configuration and get token
            with open(config_path, 'r') as f:
                config = json.load(f)
                main_logger.info(f"Loaded config: {config}")
            
            access_token = graph_access_token(
                client_id=config["client_id"],
                client_secret=config["client_secret"],
                tenant_id=config["tenant_id"]
            )
            main_logger.info(f"Access token obtained: {access_token}")
        else:
            # ASIO environment handling
            main_logger.info("Running in ASIO environment")
            temp_logger = Logger()
            access_token = get_access_token(temp_logger)
            main_logger.info(f"Access token obtained: {access_token}")
            if not access_token:
                exception_msg = "Failed to obtain access token"
                main_logger.result_failed_message(exception_msg)

        # Create and initialize orchestrator
        try:
            main_logger.info("Creating orchestrator")
            orchestrator = await UserManagementOrchestrator.create(
                log_level=logging.DEBUG, 
                access_token=access_token,
                input_form=input_obj
            )
            main_logger.info("Orchestrator created successfully")
        except Exception as e:
            main_logger.result_failed_message(f"Failed to create orchestrator: {e}")
            main_logger.close()
            raise
            
        # Run main process
        await orchestrator.run()
        
    except Exception as e:
        main_logger.result_failed_message(f"Critical error in main: {e}")
        main_logger.close()
        raise
    
    main_logger.close()

if __name__ == "__main__":
    asyncio.run(main())