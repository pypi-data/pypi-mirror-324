#!/usr/bin/env python
# -*- coding: utf-8 -*-

from m365_user_manager.core.orchestrator import UserManagementOrchestrator
from typing import Union, Optional
from cw_rpa import Logger, HttpClient, Input
import logging
import asyncio

class SyncOrchestrator:
    """
    Synchronous wrapper for UserManagementOrchestrator.
    Handles all the async/await functionality internally.
    """
    def __init__(
        self,
        access_token: str,
        log_level: int = logging.DEBUG,
        input_form: Optional[Input] = None,
        http_client: Optional[HttpClient] = None,
        logger: Optional[Logger] = None,
        running_in_asio: bool = False
    ):
        self.logger = logger or Logger()
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        
        try:
            self._orchestrator = self._loop.run_until_complete(
                UserManagementOrchestrator.create(
                    access_token=access_token,
                    log_level=log_level,
                    input_form=input_form,
                    http_client=http_client,
                    running_in_asio=running_in_asio
                )
            )
        except Exception as e:
            self.logger.error(f"Failed to create orchestrator: {e}")
            raise

    def run(self) -> dict:
        """
        Synchronously run the orchestrator process
        """
        try:
            return self._loop.run_until_complete(self._orchestrator.run())
        except Exception as e:
            self.logger.error(f"Failed to run orchestrator: {e}")
            raise
        finally:
            self._loop.close()