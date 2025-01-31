#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from typing import Dict, Any, Optional, Union
from cw_rpa import Logger, Input, HttpClient
from m365_user_manager.managers.user_manager import M365UserManager
from m365_user_manager.utils.result_handler import ResultHandler
from m365_user_manager.exceptions.exceptions import TokenManagerError
import requests
import json

def graph_access_token(client_id: str, client_secret: str, tenant_id: str) -> str:
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
        print(error_msg)
        raise TokenManagerError(error_msg, 
            status_code=getattr(e.response, 'status_code', 500)
        )

def create_m365_user(
    access_token: str,
    display_name: str,
    email_address: str,
    logger: Optional[Logger] = None,
    **kwargs
) -> Dict[str, Any]:
    """
    Create a new Microsoft 365 user with proper async handling and result processing.
    
    Args:
        access_token (str): Valid Microsoft Graph API access token
        display_name (str): User's display name
        email_address (str): User's email address
        logger (Logger, optional): Custom logger instance
        **kwargs: Additional user creation parameters including:
            - user_to_copy (str): Template user to copy from
            - copy_licenses (bool): Whether to copy licenses from template user
            - license_skus (List[str]): List of license SKUs to assign
            - groups (List[str]): List of groups to add user to
            - roles (List[str]): List of roles to assign
            - business_phone (str): Business phone number
            - mobile_phone (str): Mobile phone number
            - job_title (str): Job title
            - department (str): Department
            - office_location (str): Office location
            
    Returns:
        Dict[str, Any]: Processed result data
    """
    # Initialize logger if not provided
    if logger is None:
        logger = Logger()
    
    # Initialize result handler
    result_handler = ResultHandler(logger=logger)
    
    try:
        # Create event loop if one doesn't exist
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        
        # Initialize user manager with required parameters
        user_manager = M365UserManager(
            access_token=access_token,
            logger=logger,
            running_in_asio=False,
            api_token=kwargs.get("api_token", None),
            discord_webhook_url=kwargs.get("discord_webhook_url", None)
        )
        
        # Create coroutine for user creation
        async def create_user_coro():
            try:
                # Attempt to create the user
                result = await user_manager.create_user(
                    display_name=display_name,
                    email_address=email_address,
                    **kwargs
                )
                
                if not result:
                    logger.error("User creation failed - no result returned")
                    return None
                
                return result
                
            except Exception as e:
                logger.error(f"Error during user creation: {str(e)}")
                return None
        
        # Run the coroutine and get results
        raw_results = loop.run_until_complete(create_user_coro())
        
        if not raw_results:
            logger.error("User creation failed")
            logger.result_failed_message("User creation failed")
            return {}
        
        # Process results through Asio result handler
        processed_results = result_handler.handle_asio_result(raw_results)
        
        if not processed_results:
            logger.error("Result processing failed")
            logger.result_failed_message("Result processing failed")
            return {}
        
        # Log final results
        logger.result_data(processed_results)
        
        return processed_results
        
    except Exception as e:
        logger.error(f"Unexpected error in user creation process: {str(e)}")
        logger.result_failed_message(f"User creation failed: {str(e)}")
        return {}

def get_access_token(log: Logger, http_client: HttpClient) -> Union[str, None]:
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

def main():
    """
    Example usage of the create_m365_user function.
    """
    # Initialize logger
    logger = Logger()
    input_form = Input()
    http_client = HttpClient()
    DISPLAY_NAME = "DisplayName_1737154608192"
    EMAIL_ADDRESS = "EmailAddress_1737154657850"
    PASSWORD = "Password_1737154656469"
    JOB_TITLE = "JobTitle_1737154733788"
    DEPARTMENT = "Department_1737154731291"
    OFFICE_LOCATION = "OfficeLocation_1737154659481"
    CITY = "City_1737154742161"
    STATE = "State_1737154743922"
    BUSINESS_PHONE = "BusinessPhone_1737154735784"
    MOBILE_PHONE = "MobilePhone_1737154737302"
    GROUPS = "Groups_1737154746910"
    LICENSE_SKUS = "LicenseSKUs_1737154745588"
    USER_TO_COPY = "UserToCopy_1737154748715"
    COPY_LICENSES = "CopyLicenses_1737159741637"
    PASSWORD_PUSH_TOKEN = "PasswordPushToken_1737575340807"
    WEBHOOK_URL = "Webhook_URL_1738104979016"
    #ACCESS_TOKEN = get_access_token(log=logger, http_client=http_client)
    
    config_path = "environments/asio_365_config.json"

    # Load configuration and get token
    with open(config_path, 'r') as f:
        config = json.load(f)
        logger.info(f"Loaded config: {config}")
    
    ACCESS_TOKEN = graph_access_token(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        tenant_id=config["tenant_id"]
    )
    logger.info(ACCESS_TOKEN)
    try:
        config = {
            "access_token": ACCESS_TOKEN,
            "display_name": input_form.get_value(DISPLAY_NAME),
            "email_address": input_form.get_value(EMAIL_ADDRESS),
            "password": input_form.get_value(PASSWORD),
            "job_title": input_form.get_value(JOB_TITLE),
            "department": input_form.get_value(DEPARTMENT),
            "office_location": input_form.get_value(OFFICE_LOCATION),
            "city": input_form.get_value(CITY),
            "state": input_form.get_value(STATE),
            "business_phone": input_form.get_value(BUSINESS_PHONE),
            "mobile_phone": input_form.get_value(MOBILE_PHONE),
            "groups": input_form.get_value(GROUPS),
            "license_skus": input_form.get_value(LICENSE_SKUS),
            "user_to_copy": input_form.get_value(USER_TO_COPY),
            "copy_licenses": input_form.get_value(COPY_LICENSES),
            "api_token": input_form.get_value(PASSWORD_PUSH_TOKEN),
            "discord_webhook_url": input_form.get_value(WEBHOOK_URL)
        }
        logger.info(config)
        # Create the user
        results = create_m365_user(
            logger=logger,
            **config
        )
        
        # Check results
        if results:
            logger.info("User creation completed successfully")
        else:
            logger.error("User creation process failed")
            
    except Exception as e:
        logger.error(f"Main process failed: {str(e)}")
        logger.result_failed_message(f"Process failed: {str(e)}")

if __name__ == "__main__":
    main()