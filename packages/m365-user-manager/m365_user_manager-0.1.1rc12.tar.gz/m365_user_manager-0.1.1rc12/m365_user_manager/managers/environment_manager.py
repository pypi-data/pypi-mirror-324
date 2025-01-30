#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ./m365_user_manager/managers/environment_manager.py

from typing import Dict, Optional, Set
from pathlib import Path
import json
from cw_rpa_unified_logger import get_logger
import logging

class EnvironmentManager():
    """
    Manages environment configuration and setup for the application.
    
    This class handles environment detection (local vs Asio RPA), logging setup,
    and configuration management. It maintains a predefined list of Microsoft 365
    product licenses and their corresponding SKU IDs.
    
    Usage:
        env_manager = EnvironmentManager()
        is_asio, config = env_manager.initialize()
        
        # Access logger
        env_manager.logger.info("Application started")
        
    Attributes:
        PRODUCT_LICENSES (List[Dict]): Mapping of M365 license names to SKU IDs
        access_token (bool): Indicates if running in Asio environment
        config (Dict): Configuration parameters loaded from file
        logger (Logger): Logging instance for the application
        
    Methods:
        initialize(): Sets up environment and returns (is_asio, config)
        setup_logging(): Configures logging handlers
        determine_environment(): Detects runtime environment
    """
    PRODUCT_LICENSES = [
        {"ProductName": "Microsoft 365 E1", "StringID": "STANDARDPACK"},
        {"ProductName": "Microsoft 365 E3", "StringID": "SPE_E3"},
        {"ProductName": "Microsoft 365 E5", "StringID": "SPE_E5"},
        {"ProductName": "Microsoft 365 Business Basic", "StringID": "O365_BUSINESS_ESSENTIALS"},
        {"ProductName": "Microsoft 365 Business Standard", "StringID": "O365_BUSINESS_PREMIUM"},
        {"ProductName": "Microsoft 365 Business Premium", "StringID": "SPB"},
        {"ProductName": "Microsoft Defender for Endpoint", "StringID": "DEFENDER_ENDPOINT_P1"},
        {"ProductName": "Power Automate Free", "StringID": "FLOW_FREE"},
        {"ProductName": "Power Automate Premium", "StringID": "POWERAUTOMATE_ATTENDED_RPA"},
        {"ProductName": "Power BI Pro", "StringID": "POWER_BI_PRO"},
        {"ProductName": "Microsoft Teams Essentials", "StringID": "Teams_Ess"},
        {"ProductName": "Exchange Online Plan 1", "StringID": "EXCHANGESTANDARD"},
        {"ProductName": "Exchange Online Plan 2", "StringID": "EXCHANGEENTERPRISE"},
        {"ProductName": "Copilot for Microsoft 365", "StringID": "Microsoft_365_Copilot"}
    ]

    def __init__(self, discord_webhook_url: Optional[str] = None, 
                 access_token: Optional[bool] = None,
                 enabled_loggers: Optional[Set[str]] = None, log_level: Optional[int] = None):
        """Initialize basic attributes without depending on logger."""
        self.access_token = access_token
        self.discord_webhook_url = discord_webhook_url
        self.enabled_loggers = enabled_loggers or {"local", "asio"}
        self.logger = None  # Will be set by setup_logging
        self.config = None
        self.configuration_path = None
        self.log_level = log_level or logging.INFO
        
    async def setup_logging(self) -> Optional[logging.Logger]:
        """Set up logging with async support."""
        try:
            if self.discord_webhook_url:
                print(f"Setting up logger with Discord webhook: {self.discord_webhook_url}")
                logger, manager = await get_logger(
                    webhook_url=self.discord_webhook_url,
                    log_level=self.log_level,
                    logger_types=self.enabled_loggers,
                    enable_terminal=True,
                    terminal_level=logging.WARNING
                )
                
                if not logger:
                    print("Warning: Logger returned by get_logger is None.")
                else:
                    print("Discord logger initialized successfully.")
                return logger
            else:
                print("Discord webhook URL not provided. Setting up local/asio loggers.")
                updated_logger_types = self.enabled_loggers - {"discord"}
                logger, manager = await get_logger(
                    webhook_url=None,
                    log_level=self.log_level,
                    logger_types=updated_logger_types,
                    enable_terminal=True,
                    terminal_level=logging.WARNING
                )
                if not logger:
                    print("Warning: Logger returned by get_logger is None.")
                else:
                    print("Local/asio logger initialized successfully.")
                return logger
        except Exception as e:
            print(f"Logger setup failed: {e}")
            return None




    async def initialize(self) -> Optional[Dict]:
        """Complete async initialization sequence."""
        try:
            # First set up logging
            self.logger = await self.setup_logging()
            if not self.logger:
                print("Failed to initialize logger")
                return None

            self.logger.info("Logger initialized, setting up configuration")

            # Set up configuration path
            self.configuration_path = await self._get_configuration_path()
            if not self.configuration_path:
                self.logger.warning("Configuration path not found.")

            # Determine environment
            self.config = await self._determine_environment()

            return self.config

        except Exception as e:
            print(f"Environment initialization failed: {e}")
            return None



    async def _get_configuration_path(self) -> Optional[Path]:
        """Get configuration path with logger support."""
        if self.access_token:
            return None
            
        try:
            current = Path(__file__).resolve()
            config_name = "asio_365_config.json"
            
            for env_dir in ["environments", "Environments"]:
                config_path = current.parent.parent / env_dir / config_name
                print(f"Checking path: {config_path}")
                if config_path.exists():
                    self.logger.info(f"Found config at path: {config_path}")
                    return config_path
                    
            self.logger.warning("No configuration file found")
            return None
                
        except Exception as e:
            self.logger.error(f"Error finding configuration path: {e}")
            return None

    async def _determine_environment(self) -> Optional[Dict]:
        """Load configuration with proper async support."""
        if self.access_token:
            return None

        try:
            if not self.configuration_path:
                self.logger.warning("No configuration path set")
                return None

            with open(self.configuration_path, 'r') as f:
                config = json.load(f)

            # Validate required keys
            required_keys = ['client_id', 'client_secret', 'tenant_id']
            if all(key in config for key in required_keys):
                self.logger.info("Valid configuration loaded")
                return config

            self.logger.error("Configuration missing required keys")
            return None

        except Exception as e:
            self.logger.error(f"Error loading configuration: {e}")
            return None
                
        except Exception as e:
            self.logger.error(f"Error finding configuration path: {str(e)}")
            return None

    def determine_environment(self) -> Optional[Dict]:
        """Load configuration if not running in Asio."""
        if self.access_token:
            return None
            
        try:
            if not self.configuration_path:
                self.logger.warning("No configuration path found")
                return None
                
            with open(self.configuration_path, 'r') as f:
                config = json.load(f)
                
            # Validate required keys
            required_keys = ['client_id', 'client_secret', 'tenant_id']
            if all(key in config for key in required_keys):
                return config
                
            self.logger.error("Configuration file missing required keys")
            return None

        except (FileNotFoundError, json.JSONDecodeError) as e:
            self.logger.error(f"Error loading configuration: {str(e)}")
            return None