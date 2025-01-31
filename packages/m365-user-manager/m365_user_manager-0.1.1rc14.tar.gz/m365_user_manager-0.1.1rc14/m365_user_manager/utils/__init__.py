"""
M365 User Manager utility modules for processing inputs and handling results.

Contains:
  - InputProcessor: Handles and validates user input data for M365 operations
  - ResultHandler: Processes and formats results from M365 API operations

This module provides the core utilities needed for managing Microsoft 365 user data
by exposing classes that handle input validation and result processing.
"""
from m365_user_manager.utils.input_processor import InputProcessor
from m365_user_manager.utils.result_handler import ResultHandler
from m365_user_manager.utils.input_identifiers import FormFields

__all__ = ["InputProcessor", "ResultHandler", "FormFields"]