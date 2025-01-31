#!/usr/bin/env python
# -*- coding: utf-8 -*-

from m365_user_manager.core import SyncOrchestrator  # You'll need to add SyncOrchestrator to your imports
import logging
from m365_user_manager.exceptions.exceptions import TokenManagerError
import requests
from cw_rpa import Logger, Input, HttpClient
import json

main_logger = Logger()

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

def main():
    try:
        # Initialize Input handling first
        input_obj = Input()
        http_client = HttpClient()
        main_logger.info("Input object initialized")
        main_logger.info(getattr(input_obj, '_data', None))
        
        # Handle access token for local environment
        main_logger.info("Running in local environment")
        config_path = "environments/asio_365_config.json"

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

        # Create and initialize orchestrator
        try:
            main_logger.info("Creating orchestrator")
            orchestrator = SyncOrchestrator(
                access_token=access_token,
                log_level=logging.DEBUG,
                input_form=input_obj,
                http_client=http_client,
                logger=main_logger,
                running_in_asio=False
            )
            main_logger.info("Orchestrator created successfully")
        except Exception as e:
            main_logger.result_failed_message(f"Failed to create orchestrator: {e}")
            main_logger.close()
            raise
            
        # Run main process
        result_data = orchestrator.run()  # No await needed
        main_logger.info(f"Result data: {json.dumps(result_data, indent=2)}")
        main_logger.result_data(result_data)
        
    except Exception as e:
        main_logger.result_failed_message(f"Critical error in main: {e}")
        raise
    finally:
        main_logger.close()

if __name__ == "__main__":
    main()