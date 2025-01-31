from m365_user_manager.managers.request_manager import RequestManager
from m365_user_manager.managers.cache_manager import CacheManager
from typing import Dict, List, Optional
from logging import Logger

class MembershipManager:
    """Handles user group and role membership operations."""
    
    def __init__(self, request_manager: RequestManager, cache_manager: CacheManager, logger: Optional[Logger] = None):
        self.request_manager = request_manager
        self.cache_manager = cache_manager
        self.logger = logger

    async def get_user_memberships(self, user_id: str) -> Dict[str, List[Dict]]:
        """Get user's group and role memberships."""
        try:
            response = await self.request_manager.make_request(
                "GET", f"users/{user_id}/memberOf"
            )
            memberships = response.json().get('value', [])
            
            return {
                'groups': [m for m in memberships if m.get('@odata.type') == '#microsoft.graph.group'],
                'roles': [m for m in memberships if m.get('@odata.type') == '#microsoft.graph.directoryRole']
            }
        except Exception as e:
            self.logger.error(f"Failed to get user memberships: {e}")
            return {'groups': [], 'roles': []}

    async def add_user_to_group(self, user_id: str, group_id: str) -> bool:
        """Add user to specified group."""
        try:
            await self.request_manager.make_request(
                "POST",
                f"groups/{group_id}/members/$ref",
                json_data={
                    "@odata.id": f"{self.request_manager.graph_endpoint}/directoryObjects/{user_id}"
                }
            )
            return True
        except Exception as e:
            self.logger.error(f"Failed to add user to group: {e}")
            return False