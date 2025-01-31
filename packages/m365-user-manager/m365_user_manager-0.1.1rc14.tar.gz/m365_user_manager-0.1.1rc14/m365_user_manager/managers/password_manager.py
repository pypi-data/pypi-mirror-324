#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ./m365_user_manager/managers/password_manager.py

from typing import Optional
import requests
import random
import string
import json
from m365_user_manager.managers.environment_manager import EnvironmentManager
from m365_user_manager.exceptions.exceptions import PasswordManagerError
from logging import Logger

class PasswordManager:
    """
    Handles password generation and secure sharing functionality.
    
    Provides methods for generating secure passwords and creating secure one-time links
    for password sharing using Password Pusher service with fallback to onetimesecret.com.
    
    Attributes:
        MIN_PASSWORD_LENGTH: Minimum length for generated passwords
        MAX_TTL: Maximum time-to-live in days for shared secrets
        MAX_TTL_SECONDS: Maximum time-to-live in seconds
    """
    def __init__(self, discord_webhook_url: Optional[str] = None, logger: Optional[Logger] = None, config: Optional[dict] = None, api_token: Optional[str] = None, access_token: Optional[str] = None):
        """Initialize password manager with environment configuration and logging."""
        self.discord_webhook_url = discord_webhook_url
        self.logger = logger
        self.config = config
        self.api_token = api_token if api_token else "QB5JxHEX6JznDjGhvTmZ6US9"
        self.access_token = access_token
        self.logger.info(f"API token in password manager: {self.api_token}")
        

        self.MIN_PASSWORD_LENGTH = 12
        self.MAX_TTL = 5
        self.MAX_TTL_SECONDS = self.MAX_TTL * 86400

    @classmethod
    async def create(cls, discord_webhook_url: Optional[str] = None, logger: Optional[Logger] = None, access_token: Optional[str] = None) -> 'PasswordManager':
        env_manager = EnvironmentManager(discord_webhook_url=discord_webhook_url, access_token=access_token)
        config = await env_manager.initialize()
        return cls(discord_webhook_url, logger, config)

    def generate_secure_password(self) -> str:
        """
        Generate a secure password with mixed characters.
        
        Returns:
            str: Generated password containing mixed case letters, numbers and symbols
            
        Raises:
            PasswordManagerError: If password generation fails
        """
        try:
            chars = {
                'uppercase': string.ascii_uppercase,
                'lowercase': string.ascii_lowercase,
                'digits': string.digits,
                'special': "!@#$%^&*()_+-="
            }
            
            password = [
                random.choice(chars['uppercase']),
                random.choice(chars['lowercase']),
                random.choice(chars['digits']),
                random.choice(chars['special'])
            ]
            
            all_chars = ''.join(chars.values())
            password.extend(random.choices(
                all_chars,
                k=self.MIN_PASSWORD_LENGTH - len(password)
            ))
            
            random.shuffle(password)
            return ''.join(password)
            
        except Exception as e:
            error_msg = f"Failed to generate secure password: {str(e)}"
            self.logger.error(error_msg)
            raise PasswordManagerError(error_msg, code=500)

    def create_secure_link(self, secret: str, ttl_days: int = 3) -> str:
        """
        Create a secure one-time link using Password Pusher service, falling back to onetimesecret.com.

        Args:
            secret: The secret text/password to share
            ttl_days: Time to live in days (default 3, max 5)

        Returns:
            str: URL for accessing the shared secret

        Raises:
            PasswordManagerError: If link creation fails or input validation fails
        """
        if not secret:
            raise PasswordManagerError("Cannot create secure link: secret cannot be empty", code=400)
            
        if not isinstance(ttl_days, int) or ttl_days <= 0:
            raise PasswordManagerError("TTL must be a positive integer in days", code=400)
            
        ttl_days = min(ttl_days, self.MAX_TTL)

        try:
            # Use self.api_token directly
            api_token = self.api_token

            self.logger.debug(f"Using self.api_token: {api_token}")

            if not api_token:
                self.logger.info("No Password Pusher token available, using backup service")
                return self.backup_secure_link(secret, ttl_days)

            url = 'https://pwpush.com/p.json'
            headers = {'Accept': 'application/json', 'Authorization': f"Bearer {api_token}"}
            data = {
                'password[payload]': secret,
                'password[expire_after_days]': ttl_days,
                'password[expire_after_views]': 3
            }
            
            response = requests.post(url, headers=headers, data=data, timeout=30)
            
            if response.status_code in [401, 429]:
                self.logger.warning(f"Password Pusher responded with status {response.status_code}. Using backup service.")
                return self.backup_secure_link(secret, ttl_days)
                
            response.raise_for_status()
            result = response.json()
            
            url = result.get('html_url') or f"https://pwpush.com/p/{result['url_token']}/r"
            return url
                
        except (requests.exceptions.RequestException, KeyError, ValueError, json.JSONDecodeError) as e:
            self.logger.error(f"Error creating secure link with Password Pusher: {str(e)}. Using backup service.")
            return self.backup_secure_link(secret, ttl_days)


    def backup_secure_link(self, secret: str, ttl_days: int) -> str:
        """
        Create a secure one-time link using onetimesecret.com service.

        Args:
            secret: The secret text/password to share
            ttl_days: Time to live in days (will be converted to seconds)

        Returns:
            str: URL for the one-time secret

        Raises:
            PasswordManagerError: If link creation fails or input validation fails
        """
        ttl = ttl_days * 86400

        if not secret:
            raise PasswordManagerError("Cannot create secure link: secret cannot be empty", code=400)

        if not isinstance(ttl, int) or ttl <= 0:
            raise PasswordManagerError("TTL must be a positive integer", code=400)

        ttl = min(ttl, self.MAX_TTL_SECONDS)

        try:
            response = requests.post(
                'https://onetimesecret.com/api/v1/share',
                data={'secret': secret, 'ttl': ttl},
                timeout=30,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )

            if response.status_code == 429:
                raise PasswordManagerError("Rate limit exceeded. Please try again later.", code=429)

            if response.status_code == 413:
                raise PasswordManagerError("Secret exceeds maximum allowed size", code=413)

            response.raise_for_status()
            result = response.json()
            
            if 'secret_key' not in result:
                raise PasswordManagerError("Invalid response from service: missing secret_key", code=500)

            return f"https://onetimesecret.com/secret/{result['secret_key']}"

        except requests.exceptions.Timeout:
            raise PasswordManagerError("Timeout while creating secure link", code=408)

        except requests.exceptions.RequestException as e:
            raise PasswordManagerError(
                f"Error creating secure link: {str(e)}",
                code=getattr(e.response, 'status_code', 500)
            )

        except (KeyError, ValueError, json.JSONDecodeError) as e:
            raise PasswordManagerError(f"Error processing service response: {str(e)}", code=500)