#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ./m365_user_manager/core/orchestrator.py


from typing import Dict, Optional, Any
from cw_rpa import HttpClient, Input
import json
from m365_user_manager.utils.input_processor import InputProcessor
from m365_user_manager.managers.environment_manager import EnvironmentManager
from m365_user_manager.managers.user_manager import M365UserManager
from m365_user_manager.utils.result_handler import ResultHandler
from m365_user_manager.utils.input_identifiers import FormFields

class UserManagementOrchestrator():
    """
    Orchestrates the entire user management workflow.
    
    Coordinates between different components (EnvironmentManager, InputProcessor,
    TokenManager, etc.) to execute the complete user management process.
    
    Usage:
        orchestrator = UserManagementOrchestrator()
        orchestrator.run()
        
    Methods:
        run(): Executes the complete user management workflow
    """
    def __init__(self, access_token: bool = False, config: dict = None, enabled_loggers: set = None, log_level: int = None, input_form: Optional[Input] = None, http_client: Optional[HttpClient] = None, running_in_asio: bool = False):
        self.config = config
        self.input_form = input_form or Input()
        self.input_ids = FormFields()
        self.discord_webhook_id = self.input_ids.WEBHOOK_URL
        self.api_token_id = self.input_ids.PASSWORD_PUSH_TOKEN
        self.api_token = self.return_api_token()
        self.discord_webhook_url = self.return_webhook_url()
        self.integration_name = "azure_o365"
        self.logger = None  # Will be set up during initialization
        self.log_level = log_level
        self.enabled_loggers = enabled_loggers or {"local", "asio"}
        self.access_token = access_token
        self.http_client = http_client
        self.running_in_asio = running_in_asio
        

    @classmethod
    async def create(cls, access_token: bool = False, config: dict = None, log_level: int = None, input_form: Optional[Input] = None, http_client: HttpClient = None, running_in_asio: bool = False) -> 'UserManagementOrchestrator':
        """Async factory method for creating fully initialized instances."""
        instance = cls(access_token, config, log_level=log_level, input_form=input_form, http_client=http_client, running_in_asio=running_in_asio)
        await instance.initialize()
        return instance

    async def initialize(self) -> None:
        """Async initialization of components."""
        try:
            # Initialize environment manager first
            self.env_manager = EnvironmentManager(
                discord_webhook_url=self.discord_webhook_url,
                access_token=self.access_token,
                enabled_loggers=self.enabled_loggers,
                log_level=self.log_level
            )
            
            # Initialize environment (includes logger setup)
            self.config = await self.env_manager.initialize()
            if not self.config and not self.access_token:
                raise RuntimeError("Failed to initialize environment configuration.")
            
            # Now we can safely use the logger
            self.logger = self.env_manager.logger
            self.logger.info(f"API token in orchestrator: {self.api_token}")
            self.logger.info(f"Initialized loggers: {self.logger.config}")
            if not self.logger:
                raise RuntimeError("Failed to initialize logger")

            self.logger.debug(f"Webhook URL: {self.discord_webhook_url}")
            self.logger.info("Environment setup complete, initializing remaining components")
            
            # Initialize other components
            self.input_processor = await InputProcessor.create(
                discord_webhook_url=self.discord_webhook_url,
                logger=self.logger,
                input_form=self.input_form,
                http_client=self.http_client
            )
            
            self.result_handler = ResultHandler(discord_webhook_url=self.discord_webhook_url, logger=self.logger)
            
            self.logger.info("Orchestrator initialization complete")

        except Exception as e:
            print(f"Orchestrator initialization failed: {e}")
            raise

    def return_api_token(self):
        try:
            api_token = self.input_form.get_value(self.api_token_id)
            if not api_token:
                print("Warning: API token is None or empty.")
            else:
                print(f"API token retrieved: {api_token}")
            return api_token
        except Exception as e:
            print(f"Error retrieving API token: {str(e)}")
            return None

    def return_webhook_url(self):
        try:
            webhook_url = self.input_form.get_value(self.discord_webhook_id)
            if not webhook_url:
                print("Warning: Webhook URL is None or empty.")
            else:
                print(f"Webhook URL retrieved: {webhook_url}")
            return webhook_url
        except Exception as e:
            print(f"Error retrieving webhook URL: {str(e)}")
            return None

    async def run(self):
        """Run the user management process with async support."""
        try:
            self.logger.info("Starting orchestration process")
            
            # Await process_input() since it's a coroutine
            kwargs, error = await self.input_processor.process_input()
            if error:
                self.logger.error(f"Input processing error: {error}")
                self.logger.result_failed_message(error)
                return
            
            self._debug_input_parameters(kwargs)

            self.logger.info("Input processed successfully")
            self.logger.debug(f"Input parameters: {json.dumps(kwargs, indent=2)}")

            # Token acquisition
            if not self.access_token:
                error = "Failed to obtain authentication token"
                self.logger.error(error)
                self.logger.result_failed_message(error)
                return

            self.logger.info("Authentication token obtained successfully")

            # User creation now uses await
            user_manager = M365UserManager(
                logger=self.logger,  # Pass the same logger instance
                product_licenses=self.env_manager.PRODUCT_LICENSES,
                access_token=self.access_token,
                http_client=self.http_client,  # Ensure http_client is passed
                discord_webhook_url=self.discord_webhook_url,
                api_token=self.api_token,
                running_in_asio=self.running_in_asio
            )
            
            self.logger.info("Starting user creation process")
            result = await user_manager.create_user(**kwargs)
            
            # Validate the result structure
            if result and self._validate_result_structure(result):
                self.logger.info("User creation completed successfully")
                self.logger.debug(f"User creation result: {json.dumps(result, indent=2)}")
                
            else:
                error_msg = "User creation failed or returned invalid result"
                self.logger.error(error_msg)
                raise RuntimeError(error_msg)
            
            # Handle the result
            result_data = self.handle_result(result)
            self.logger.info("Orchestration process completed successfully")
            self.logger.result_data(result_data)
            return result_data

        except Exception as e:
            self.logger.error(f"Orchestration process failed: {str(e)}", exc_info=True)
            self._handle_error(str(e))


     
    def handle_result(self, result: Optional[Dict[str, Any]]) -> None:
        """Handle operation result based on environment."""
        try:
            result_data = self.result_handler.handle_asio_result(result)
            self.result_handler.handle_local_result(result)
            return result_data
        except Exception as e:
            self.logger.error(f"Failed to handle result: {str(e)}")
            self.logger.result_failed_message(f"Result handling failed: {str(e)}")

    def _handle_error(self, error_msg: str) -> None:
        """Handle errors based on environment."""
        if self.access_token:
            self.logger.error(error_msg)
            self.logger.result_failed_message(error_msg)
        else:
            self.logger.error(error_msg)
            raise RuntimeError(error_msg)
        
    def _debug_input_parameters(self, kwargs: Dict[str, Any]) -> None:
        """Debug input parameters."""
        self.logger.info("Debugging input parameters:")
        self.logger.info(f"Display Name: {kwargs.get('display_name')}")
        self.logger.info(f"Email: {kwargs.get('email_address')}")
        self.logger.info(f"User to Copy: {kwargs.get('user_to_copy')}")
        self.logger.info(f"Copy Licenses Flag: {kwargs.get('copy_licenses')}")
        self.logger.info(f"Groups to Add: {kwargs.get('groups')}")
        self.logger.info(f"License SKUs: {kwargs.get('license_skus')}")
        
    def _validate_result_structure(self, result: Dict[str, Any]) -> bool:
        """Validate the basic structure of the user creation result."""
        required_fields = ['id', 'email', 'password', 'displayName', 'password_link']
        required_nested = {
            'groups': ['successful', 'failed'],
            'licenses': ['available', 'unavailable', 'available_str', 'unavailable_str'],
            'roles': ['successful', 'failed']
        }
        
        try:
            # Check base fields
            if not all(field in result for field in required_fields):
                self.logger.error(f"Missing required fields in result. Expected: {required_fields}")
                return False
                
            # Check nested structures
            for key, fields in required_nested.items():
                if key not in result or not isinstance(result[key], dict):
                    self.logger.error(f"Missing or invalid nested structure: {key}")
                    return False
                if not all(field in result[key] for field in fields):
                    self.logger.error(f"Missing required fields in {key}: {fields}")
                    return False
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Result validation failed: {str(e)}")
            return False