#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ./m365_user_manager/utils/result_handler.py

from typing import Any, Dict, Optional
import json
from pathlib import Path
from cw_rpa import Logger
import logging
class ResultHandler:
    """
    Manages operation results and output formatting for M365 user operations.
    
    Provides consistent result handling for both local and Asio environments with
    standardized success/failure tracking and detailed logging.
    
    Attributes:
        discord_webhook_url (str): Optional Discord webhook for notifications
        logger (Logger): Logger instance for output handling
        
    Usage:
        handler = ResultHandler(logger=custom_logger)
        handler.handle_local_result(operation_result)
        # or
        handler.handle_asio_result(operation_result)
    """
    
    def __init__(self, discord_webhook_url: Optional[str] = None, 
                 logger: Optional[logging.Logger] = None) -> None:
        self.discord_webhook_url = discord_webhook_url
        self.logger = logger
        
    def _validate_result(self, result: Dict[str, Any]) -> bool:
        """Validate that the result contains required fields."""
        try:
            # Check for base required fields
            required_fields = ['id', 'email', 'password', 'displayName', 'password_link']
            if not all(field in result for field in required_fields):
                return False
            
            # Check for nested structures
            required_nested = {
                'groups': ['successful', 'failed'],
                'licenses': ['available', 'unavailable', 'available_str', 'unavailable_str'],
                'roles': ['successful', 'failed']
            }
            
            for key, fields in required_nested.items():
                if key not in result or not isinstance(result[key], dict):
                    return False
                if not all(field in result[key] for field in fields):
                    return False
                    
            return True
            
        except Exception as e:
            self.logger.error(f"Result validation failed: {str(e)}")
            return False

    def return_result(self, result: Dict[str, Any]) -> None:
        """Return the result to the calling environment."""
        result_data = {
                "user_id": result["id"],
                "status": "success",
                "message": "User created successfully",
                "email": result["email"],
                "display_name": result["displayName"],
                "password": result["password"],
                "password_link": result["password_link"],
                "licenses": {
                    "successful": [lic for lic in result['licenses']['available']],
                    "failed": result["licenses"]["unavailable"],
                    "successful_str": result["licenses"]["available_str"],
                    "failed_str": result["licenses"]["unavailable_str"]
                },
                "groups": {
                    "successful": result["groups"]["successful"],
                    "failed": result["groups"]["failed"]
                },
                "roles": {
                    "successful": result["roles"]["successful"],
                    "failed": result["groups"]["failed"]
                }
            }
        return result_data

    def handle_asio_result(self, result: Dict[str, Any]) -> None:
        """Process results in Asio environment with standardized structure."""
        self.logger = Logger()
        if not result or not self._validate_result(result):
            self.logger.error("User creation failed - invalid result structure")
            self.logger.result_failed_message("User creation failed")
            return

        try:
            # Map the result to match the expected structure
            result_data = {
                "user_id": result["id"],
                "status": "success",
                "message": "User created successfully",
                "email": result["email"],
                "display_name": result["displayName"],
                "password": result["password"],
                "password_link": result["password_link"],
                "licenses": {
                    "successful": [lic for lic in result['licenses']['available']],
                    "failed": result["licenses"]["unavailable"],
                    "successful_str": result["licenses"]["available_str"],
                    "failed_str": result["licenses"]["unavailable_str"]
                },
                "groups": {
                    "successful": result["groups"]["successful"],
                    "failed": result["groups"]["failed"]
                },
                "roles": {
                    "successful": result["roles"]["successful"],
                    "failed": result["groups"]["failed"]
                }
            }

            self.logger.info(f"Result data: {json.dumps(result_data, indent=2)}")
            
            return result_data
            
        except Exception as e:
            self.logger.error(f"Failed to process Asio result: {str(e)}")
            self.logger.result_failed_message(f"Result processing failed: {str(e)}")

    def handle_local_result(self, result: Dict[str, Any]) -> None:
        """Process results in local environment with detailed logging."""
        if not result or not self._validate_result(result):
            self.logger.error("User creation failed - invalid result structure")
            return

        try:
            # Basic user information
            self.logger.info("\nUser created successfully!")
            self.logger.info(f"Display Name: {result['displayName']}")
            self.logger.info(f"Email: {result['email']}")
            self.logger.info(f"Initial password: {result['password']}")
            self.logger.info(f"Password link: {result['password_link']}")
            
            # License information
            self._log_section(
                "License Status",
                f"Available:\n{result['licenses']['available_str']}\n\n" +
                f"Unavailable:\n{result['licenses']['unavailable_str']}"
            )
            
            # Group memberships
            self._log_section(
                "Group Assignments",
                f"Successful:\n{', '.join(result['groups']['successful'])}\n\n" +
                f"Failed:\n{', '.join(result['groups']['failed'])}" if result['groups']['failed'] else ""
            )
            
            # Role assignments
            self._log_section(
                "Role Assignments",
                f"Successful:\n{', '.join(result['roles']['successful'])}\n\n" +
                f"Failed:\n{', '.join(result['roles']['failed'])}" if result['roles']['failed'] else ""
            )

            # Save result to file
            self._save_result_to_file(result)
            
        except Exception as e:
            self.logger.error(f"Failed to process local result: {str(e)}")

    def _log_section(self, title: str, content: str) -> None:
        """Log a formatted section with title and content."""
        self.logger.info(f"\n{title}:\n{content}")
        
    def _save_result_to_file(self, result: Dict[str, Any]) -> None:
        """Save the result data to a JSON file."""
        try:
            output_file = Path(__file__).parent / "results" / "user_result.json"
            with output_file.open("w") as file:
                json.dump(result, file, indent=2)
            self.logger.info(f"Result data saved to {output_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save result data: {str(e)}")