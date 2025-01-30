from typing import Optional, List

class GraphAPIError(Exception):
    """
    Exception raised for Microsoft Graph API operation failures.
    
    Handles various Graph API related errors including:
    - Request failures
    - Rate limiting
    - Invalid operations
    - Resource not found
    - Service unavailability
    
    Usage:
        try:
            response = self._make_request("POST", "users", json_data=user_payload)
        except GraphAPIError as e:
            logging.error(f"Graph API operation failed: {str(e)}")
            
    Attributes:
        message (str): Explanation of the error
        status_code (Optional[int]): HTTP status code if applicable
        request_id (Optional[str]): Microsoft request ID for troubleshooting
    """
    def __init__(self, message: str, status_code: Optional[int] = None, 
                 request_id: Optional[str] = None):
        self.message = message
        self.status_code = status_code
        self.request_id = request_id
        super().__init__(self.message)
        
class TokenManagerError(Exception):
    """
    Exception raised for authentication and token-related failures.
    
    Handles errors related to OAuth token operations including:
    - Token acquisition failures
    - Invalid credentials
    - Token refresh errors
    - Scope permission issues
    
    Usage:
        try:
            token = token_manager.get_access_token(client_id, client_secret, tenant_id)
        except TokenManagerError as e:
            logging.error(f"Token operation failed: {str(e)}")
            
    Attributes:
        message (str): Explanation of the error
        status_code (Optional[int]): HTTP status code if applicable
    """
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
        
class PasswordManagerError(Exception):
    """
    Exception raised for errors in password management operations.
    
    This exception is raised when password-related operations fail, such as:
    - Password generation failures
    - Secure link creation errors
    - Password validation issues
    - One-time secret service connectivity problems
    
    Usage:
        try:
            password_link = password_manager.create_secure_link(secret)
        except PasswordManagerError as e:
            logging.error(f"Password operation failed: {str(e)}")
            
    Attributes:
        message (str): Explanation of the error
        code (Optional[int]): Error code if applicable
    """
    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        self.code = code
        super().__init__(self.message)
        
class InsufficientPermissionsError(Exception):
    """
    Exception raised when attempting operations without required permissions.
    
    Handles authorization-related failures including:
    - Missing role assignments
    - Insufficient scope permissions
    - Tenant access restrictions
    - Resource access denials
    
    Usage:
        try:
            result = user_manager.assign_licenses(user_id, licenses)
        except InsufficientPermissionsError as e:
            logging.error(f"Permission denied: {str(e)}")
            
    Attributes:
        message (str): Explanation of the error
        required_permissions (Optional[List[str]]): List of missing required permissions
        current_permissions (Optional[List[str]]): List of current permissions
    """
    def __init__(self, message: str, required_permissions: Optional[List[str]] = None,
                 current_permissions: Optional[List[str]] = None):
        self.message = message
        self.required_permissions = required_permissions or []
        self.current_permissions = current_permissions or []
        super().__init__(self.message)
        
class CacheError(Exception):
    """
    Exception raised for cache-related errors.
    
    Handles cache operation failures including:
    - Cache initialization errors
    - Cache read/write failures
    - Cache eviction issues
    - Cache connection problems
    
    Usage:
        try:
            cache = CacheManager()
        except CacheError as e:
            logging.error(f"Cache operation failed: {str(e)}")
            
    Attributes:
        message (str): Explanation of the error
        code (Optional[int]): Error code if applicable
    """
    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        self.code = code
        super().__init__(self.message)