"""Core orchestration module for M365 user management.

This module provides the main orchestration functionality for managing Microsoft 365 users.
It coordinates the processes of user creation, license assignment, and group management
through the UserManagementOrchestrator class.
"""

from m365_user_manager.core.orchestrator import UserManagementOrchestrator
from m365_user_manager.core.sync_orchestrator import SyncOrchestrator

__all__ = ["UserManagementOrchestrator", "SyncOrchestrator"]

