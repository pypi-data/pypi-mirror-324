from datetime import datetime, timedelta
from typing import Any, Optional
from logging import Logger


class CacheManager:
    """Manages caching for frequently accessed M365 data."""
    
    def __init__(self, ttl_minutes: int = 30, logger: Optional[Logger] = None):
        self._cache = {}
        self.logger = logger
        self._ttl = timedelta(minutes=ttl_minutes)
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value if not expired."""
        if key in self._cache:
            data, timestamp = self._cache[key]
            if datetime.now() - timestamp < self._ttl:
                self.logger.info(f"Cache hit for key: {key}")
                return data
            self.logger.info(f"Cache entry for key {key} expired")
            del self._cache[key]
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Cache value with current timestamp."""
        self.logger.info(f"Caching data for key: {key}")
        self._cache[key] = (value, datetime.now())
    
    def clear(self) -> None:
        """Clear all cached data."""
        self.logger.info("Clearing cache")
        self._cache.clear()