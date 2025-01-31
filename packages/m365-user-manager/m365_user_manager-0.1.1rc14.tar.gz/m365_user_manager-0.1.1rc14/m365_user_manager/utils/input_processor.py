#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ./m365_user_manager/utils/input_processor.py

from m365_user_manager.utils.input_identifiers import FormFields
from cw_rpa import HttpClient, Input
from typing import Any, Optional, Tuple, Dict
import json
from logging import Logger

class InputProcessor:
    """
    Processes and validates input parameters from Input form.
    
    Handles input processing logic for form inputs, providing consistent 
    parameter formatting.
    
    Usage:
        processor = await InputProcessor.create(discord_webhook_url="url")
        kwargs, error = await processor.process_input()
    """
    def __init__(self, discord_webhook_url: Optional[str] = None, logger: Optional[Logger] = None, input_form: Optional[Input] = None, http_client: Optional[HttpClient] = None):
        """Initialize basic components. Async components initialized separately."""
        self.discord_webhook_url = discord_webhook_url
        self.logger = logger
        self.input_ids = FormFields()
        self.input_form = input_form or Input()
        self.http_client = http_client
        self.integration_name = "azure_o365"

    @classmethod
    async def create(cls, discord_webhook_url: Optional[str] = None, logger: Optional[Logger] = None, input_form: Optional[Input] = None, http_client: HttpClient = None) -> 'InputProcessor':
        """Factory method for creating fully initialized instances."""
        instance = cls(discord_webhook_url, logger, input_form, http_client)
        await instance.initialize()
        return instance

    async def initialize(self) -> None:
        """Initialize async components and logging."""
        try:
            self.logger = self.logger or Logger()
            try:
                self.logger.info("Input processor initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize CW-RPA components: {str(e)}")
                raise

        except Exception as e:
            print(f"Input processor initialization failed: {e}")  # Fallback logging
            raise

    def get_value(self, field_id: str) -> Any:
      """Get the value of a field by ID."""
      try:
          return self.input_form.get_value(field_id)
      except Exception as e:
          self.logger.error(f"Error getting value for field {field_id}: {str(e)}")
          return None

    async def _process_list_field(self, field_id: str) -> Optional[str]:
        """Process a field that should be handled as a list with validation."""
        try:
            if not self.input_form:
                raise RuntimeError("Input form not initialized")
                
            value = self.input_form.get_value(field_id)
            self.logger.debug(f"Processing list field {field_id}: {value}")
            
            if isinstance(value, list):
                processed = ','.join(str(v).strip() for v in value if v)
                self.logger.debug(f"Processed list field to: {processed}")
                return processed
            return value
            
        except Exception as e:
            self.logger.error(f"Error processing list field {field_id}: {str(e)}")
            return None

    async def _process_boolean_field(self, field_id: str) -> bool:
        """Process a field that should be handled as a boolean with validation."""
        try:
            if not self.input_form:
                raise RuntimeError("Input form not initialized")
                
            value = self.input_form.get_value(field_id)
            self.logger.debug(f"Processing boolean field {field_id}: {value}")
            
            if not value:
                return False
                
            if isinstance(value, str):
                return value.lower() in ('yes', 'true', '1')
                
            return bool(value)
            
        except Exception as e:
            self.logger.error(f"Error processing boolean field {field_id}: {str(e)}")
            return False

    async def process_input(self) -> Tuple[Dict[str, Any], Optional[str]]:
        """Process input from form with comprehensive validation."""
        if not self.logger or not self.input_form:
            return {}, "Input processor not properly initialized"
            
        try:
            self.logger.info("Starting input form processing")
            kwargs = {}

            # Process fields according to their type
            field_mapping = self.input_ids.get_field_mapping()
            
            for field_name, field_id in field_mapping.items():
                try:
                    if field_id in self.input_ids.list_fields:
                        kwargs[field_name] = await self._process_list_field(field_id)
                    elif field_id in self.input_ids.boolean_fields:
                        kwargs[field_name] = await self._process_boolean_field(field_id)
                    else:
                        kwargs[field_name] = self.input_form.get_value(field_id)
                        
                    self.logger.debug(f"Processed field {field_name}: {kwargs[field_name]}")
                        
                except Exception as e:
                    self.logger.error(f"Failed to process field {field_name}: {str(e)}")
                    kwargs[field_name] = None

            # Validate required fields
            missing_fields = [
                field_name for field_name, field_id in field_mapping.items()
                if field_id in self.input_ids.required_fields and not kwargs[field_name]
            ]
            
            if missing_fields:
                error_msg = f"Required fields missing: {', '.join(missing_fields)}"
                self.logger.error(error_msg)
                return kwargs, error_msg

            self.logger.info("Input processing completed successfully")
            self.logger.debug(f"Processed parameters: {json.dumps(kwargs, indent=2)}")
            return kwargs, None

        except Exception as e:
            error_msg = f"Failed to process input: {str(e)}"
            self.logger.error(error_msg)
            return {}, error_msg
          
