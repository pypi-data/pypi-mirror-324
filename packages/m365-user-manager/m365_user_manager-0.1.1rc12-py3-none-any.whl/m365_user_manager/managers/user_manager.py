#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ./m365_user_manager/managers/user_manager.py

from typing import Any, Dict, List, Optional, Set, Tuple, Union
from cw_rpa import HttpClient
import json
import logging
from difflib import get_close_matches

from m365_user_manager.exceptions.exceptions import CacheError, InsufficientPermissionsError
from m365_user_manager.managers.password_manager import PasswordManager
from m365_user_manager.managers.request_manager import RequestManager
from m365_user_manager.managers.cache_manager import CacheManager
from m365_user_manager.managers.membership_manager import MembershipManager

class M365UserManager:
    """Enhanced Microsoft 365 user management with caching and retry logic."""
    
    def __init__(self, access_token: str, 
                 logger: Optional[logging.Logger] = None,
                 product_licenses: Optional[List[Dict[str, Any]]] = None,
                 running_in_asio: bool = True,
                 http_client: Optional[HttpClient] = None,
                 discord_webhook_url: Optional[str] = None, api_token: Optional[str] = None):
        """Initialize user manager with enhanced components."""
        self.logger = logger
        self.api_token = api_token
        
        self.graph_api_endpoint = "https://graph.microsoft.com/v1.0"
        self.request_manager = RequestManager(
            access_token=access_token,
            graph_endpoint=self.graph_api_endpoint,
            running_in_asio=running_in_asio,
            http_client=http_client,
            logger=self.logger
        )
        
        self.cache_manager = CacheManager(logger=self.logger)
        self.membership_manager = MembershipManager(
            self.request_manager,
            self.cache_manager
        )
        
        self.password_manager = PasswordManager(
            discord_webhook_url=discord_webhook_url,
            logger=self.logger,
            api_token=self.api_token
        )
        self.product_licenses = product_licenses or []

    async def assign_roles(self, user_id: str, 
                        roles_to_assign: List[str]) -> Dict[str, List[str]]:
        """Assign roles to a user with detailed logging."""
        results = {
            "successful": [],  # Changed from "copied"
            "failed": []
        }

        if not roles_to_assign:
            self.logger.info(f"[{user_id}] No roles to assign.")
            return results

        for role_name in roles_to_assign:
            try:
                self.logger.info(f"[{user_id}] Attempting to assign role: {role_name}")
                role = await self._get_role_by_name(role_name)
                
                if not role:
                    self.logger.error(f"[{user_id}] Role not found: {role_name}")
                    results["failed"].append(f"{role_name} (not found)")
                    continue

                success = await self._assign_role_to_user(user_id, role['id'])
                if success:
                    results["successful"].append(role['displayName'])  # Changed from "copied"
                    self.logger.info(f"[{user_id}] Successfully assigned role: {role['displayName']}")
                else:
                    results["failed"].append(f"{role['displayName']} (assignment failed)")
                    self.logger.error(f"[{user_id}] Failed to assign role: {role['displayName']}")

            except Exception as e:
                self.logger.error(f"[{user_id}] Error assigning role '{role_name}': {e}")
                results["failed"].append(f"{role_name} (error: {str(e)})")

        return results

    async def get_user_licenses(self, user_id: str) -> List[Dict[str, str]]:
        """Get user's current licenses with caching."""
        self.logger.info(f"Fetching licenses for user: {user_id}")
        cache_key = f"user_licenses_{user_id}"
        
        if cached_licenses := self.cache_manager.get(cache_key):
            self.logger.info(f"Found cached licenses: {json.dumps(cached_licenses, indent=2)}")
            return cached_licenses

        try:
            response = await self.request_manager.make_request(
                "GET",
                f"users/{user_id}/licenseDetails"
            )
            
            raw_licenses = response.json().get('value', [])
            self.logger.info(f"Raw license response: {json.dumps(raw_licenses, indent=2)}")
            
            licenses = []
            for sku in raw_licenses:
                friendly_name = next(
                    (info["ProductName"] for info in self.product_licenses 
                    if info["StringID"].upper() == sku.get('skuPartNumber', '').upper()),
                    sku.get('skuPartNumber', '')
                )
                
                license_info = {
                    'skuId': sku['skuId'],
                    'friendlyName': friendly_name,
                    'skuPartNumber': sku.get('skuPartNumber', '')
                }
                licenses.append(license_info)
                self.logger.info(f"Processed license: {json.dumps(license_info, indent=2)}")

            self.cache_manager.set(cache_key, licenses)
            return licenses

        except Exception as e:
            self.logger.error(f"Failed to get user licenses: {str(e)}", exc_info=True)
            return []

    async def create_base_user(self, display_name: str, email_address: str,
                            password: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Create base user with required properties."""
        try:
            first_name, last_name = self._split_display_name(display_name)
            
            user_payload = {
                "accountEnabled": True,
                "displayName": display_name,
                "mailNickname": email_address.split("@")[0],
                "userPrincipalName": email_address,
                "passwordProfile": {
                    "forceChangePasswordNextSignIn": True,
                    "password": password or self.password_manager.generate_secure_password()
                },
                "usageLocation": "US",
                "givenName": first_name,
                "surname": last_name
            }

            response = await self.request_manager.make_request(
                "POST", "users", json_data=user_payload
            )
            created_user = response.json()
            
            return {
                "id": created_user["id"],
                "email": email_address,
                "password": user_payload["passwordProfile"]["password"],
                "displayName": display_name
            }
            
        except Exception as e:
            self.logger.error(f"Failed to create base user: {e}")
            return None

    async def create_user(self, display_name: str, email_address: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Create new M365 user with enhanced error handling and validation."""
        try:
            # Input validation
            if not self._validate_email(email_address):
                self.logger.error(f"Invalid email format: {email_address}")
                return None

            # Step 1: Initialize user with complete structure
            user_result = await self._initialize_user(
                display_name=display_name,
                email_address=email_address,
                kwargs=kwargs
            )

            if not user_result:
                return None

            try:
                # Step 2: Process template user (excluding roles)
                if template_user := kwargs.get('user_to_copy'):
                    await self._process_template_user(
                        user_result,
                        template_user,
                        kwargs.get('copy_licenses', False),
                        skip_roles=True
                    )

                # Step 3: Process direct assignments (excluding roles)
                await self._process_direct_assignments(
                    user_result,
                    kwargs,
                    skip_roles=True
                )

                # Step 4: Handle roles last (both template and direct)
                await self._process_all_roles(user_result, kwargs)

            except Exception as e:
                self.logger.error(f"Error during user setup: {e}", exc_info=True)
                # Even if we encounter an error, return the partial result
                return user_result

            return user_result

        except Exception as e:
            self.logger.error(f"User creation failed: {str(e)}", exc_info=True)
            return None

    async def assign_licenses(self, user_id: str, 
                            licenses_to_assign: Set[str]) -> Dict[str, Any]:
        """Assign licenses to user with validation and availability checking."""
        if not licenses_to_assign:
            return self._empty_license_result()

        try:
            # Get cached SKUs or fetch from API
            tenant_skus = await self._get_tenant_skus()
            
            # Process each license request
            processed_licenses = [
                await self._process_license_request(license_sku, tenant_skus)
                for license_sku in licenses_to_assign
                if license_sku
            ]
            
            # Format and execute assignment
            results = self._format_license_results(processed_licenses, tenant_skus)
            
            if results['available']:
                success = await self._assign_licenses_internal(
                    user_id, results['available']
                )
                if not success:
                    return self._failed_license_result(licenses_to_assign)
                    
            return results

        except Exception as e:
            self.logger.error(f"License assignment failed: {e}")
            return self._failed_license_result(licenses_to_assign)
   

    # Utility methods
    
    # A
    async def _add_user_to_groups(self, user_id: str, 
                                group_names: List[str]) -> Dict[str, List[str]]:
        """Add user to specified groups with optimized error handling."""
        results = {
            "successful": [],
            "failed": []
        }

        if not group_names:
            return results

        try:
            # Get current memberships first
            memberships = await self.membership_manager.get_user_memberships(user_id)
            current_groups = {g['displayName'].lower(): g['id'] 
                            for g in memberships['groups']}

            for group_name in group_names:
                try:
                    if not group_name.strip():
                        continue

                    # Skip if already a member
                    if group_name.lower() in current_groups:
                        results["successful"].append(
                            f"{group_name} (already member)"
                        )
                        continue

                    # Get group details
                    group = await self._get_group_by_name(group_name)
                    if not group:
                        results["failed"].append(f"{group_name} (not found)")
                        continue

                    # Add to group
                    success = await self.membership_manager.add_user_to_group(
                        user_id, group['id']
                    )
                    
                    if success:
                        results["successful"].append(group['displayName'])
                    else:
                        results["failed"].append(
                            f"{group['displayName']} (addition failed)"
                        )

                except Exception as e:
                    self.logger.error(f"Failed to add to group {group_name}: {e}")
                    results["failed"].append(f"{group_name} (error: {str(e)})")

        except Exception as e:
            self.logger.error(f"Group assignment process failed: {e}")
            results["failed"].append(f"Assignment process error: {str(e)}")

        return results

    async def _assign_licenses_internal(self, user_id: str, 
                                    license_details: List[Dict[str, Any]]) -> bool:
        """Internal method to assign licenses to a user."""
        self.logger.info(f"Starting internal license assignment for user: {user_id}")
        self.logger.info(f"Licenses to assign: {json.dumps(license_details, indent=2)}")
        
        try:
            if not license_details:
                self.logger.info("No licenses to assign")
                return True
                
            license_payload = {
                "addLicenses": [
                    {
                        "skuId": sku['skuId'],
                        "disabledPlans": []
                    } for sku in license_details
                ],
                "removeLicenses": []
            }
            
            self.logger.info(f"License assignment payload: {json.dumps(license_payload, indent=2)}")
            
            await self.request_manager.make_request(
                "POST",
                f"users/{user_id}/assignLicense",
                json_data=license_payload
            )
            
            self.logger.info(
                f"Successfully assigned licenses: {[sku['friendlyName'] for sku in license_details]}"
            )
            return True
            
        except Exception as e:
            self.logger.error(f"License assignment failed: {str(e)}", exc_info=True)
            if hasattr(e, 'response'):
                self.logger.error(f"Error response: {e.response.text}")
            return False

    async def _assign_role_to_user(self, user_id: str, role_id: str) -> bool:
        """Assign a directory role to a user."""
        try:
            role_assignment_url = f"directoryRoles/{role_id}/members/$ref"
            body = {
                "@odata.id": f"https://graph.microsoft.com/v1.0/users/{user_id}"
            }
            response = await self.request_manager.make_request(
                "POST",
                role_assignment_url,
                json_data=body
            )

            if response.status_code in (204, 201):
                self.logger.info(f"[{user_id}] Successfully assigned role ID {role_id}")
                return True
            else:
                self.logger.error(f"[{user_id}] Failed to assign role ID {role_id}. Status Code: {response.status_code}")
                return False
        except Exception as e:
            self.logger.error(f"[{user_id}] Failed to assign role ID {role_id}: {e}")
            return False

    # C
    async def _create_password_link(self, password: str) -> str:
        """Create secure link for password sharing."""
        return self.password_manager.create_secure_link(password, ttl_days=7)

    async def _copy_group_memberships(self, source_id: str, target_id: str, 
                                    results: Dict[str, Any]) -> None:
        """Copy group memberships from source to target user."""
        try:
            memberships = await self.membership_manager.get_user_memberships(source_id)
            self.logger.info(f"Found {len(memberships['groups'])} groups to copy")
            
            for group in memberships['groups']:
                try:
                    group_name = group.get('displayName', 'Unknown Group')
                    self.logger.info(f"Copying group: {group_name}")
                    
                    success = await self.membership_manager.add_user_to_group(
                        target_id, group['id']
                    )
                    
                    if success:
                        results["groups"]["successful"].append(group_name)
                        results["copied_properties"].append(f"Group: {group_name}")
                    else:
                        results["groups"]["failed"].append(f"{group_name} (failed)")
                        
                except Exception as e:
                    self.logger.error(f"Failed to copy group {group_name}: {e}")
                    results["groups"]["failed"].append(
                        f"{group_name} (error: {str(e)})"
                    )
                    
        except Exception as e:
            self.logger.error(f"Group membership copy failed: {e}")

    async def _copy_licenses(self, source_id: str, target_id: str, 
                            results: Dict[str, Any]) -> None:
        """Copy licenses from source to target user with improved unavailable license tracking."""
        try:
            # Get source user's licenses
            source_licenses = await self._get_user_licenses(source_id)
            if not source_licenses:
                return

            # Map licenses to SKU IDs
            sku_ids = [lic.get('skuId') for lic in source_licenses if lic.get('skuId')]
            tenant_skus = await self._get_tenant_skus()
            
            # Create mapping from skuId to StringID and track all attempted licenses
            skuid_to_stringid = {}
            attempted_licenses = []
            
            for sku in tenant_skus:
                sku_id = sku['skuId'].lower()
                sku_part_number = sku['skuPartNumber'].upper()
                
                matching_license = next(
                    (info for info in self.product_licenses 
                    if info["StringID"].upper() == sku_part_number),
                    None
                )
                
                if matching_license:
                    skuid_to_stringid[sku_id] = matching_license
                    if sku_id.lower() in [s.lower() for s in sku_ids]:
                        attempted_licenses.append(matching_license)

            # Track licenses to assign and those that are unavailable
            licenses_to_assign = set()
            unavailable_licenses = []
            
            for license_info in attempted_licenses:
                # Check if the license exists in tenant and has available seats
                matching_sku = next(
                    (sku for sku in tenant_skus 
                    if sku['skuPartNumber'].upper() == license_info["StringID"].upper()),
                    None
                )
                
                if matching_sku and matching_sku['remaining'] > 0:
                    licenses_to_assign.add(license_info["StringID"])
                    results["copied_properties"].append(f"License: {license_info['ProductName']}")
                else:
                    unavailable_licenses.append({
                        'name': license_info["ProductName"],
                        'reason': 'no licenses available' if matching_sku 
                                else 'license not available in tenant'
                    })

            # Assign available licenses
            if licenses_to_assign:
                license_results = await self.assign_licenses(target_id, licenses_to_assign)
                
                # Merge the results properly
                results["licenses"] = {
                    "available": license_results["available"],
                    "unavailable": [lic['name'] for lic in unavailable_licenses],
                    "available_str": license_results["available_str"],
                    "unavailable_str": "\n".join(
                        f"{lic['name']} ({lic['reason']})" 
                        for lic in unavailable_licenses
                    ) if unavailable_licenses else "No unavailable licenses"
                }
            else:
                # If no licenses could be assigned, update results accordingly
                results["licenses"] = {
                    "available": [],
                    "unavailable": [lic['name'] for lic in unavailable_licenses],
                    "available_str": "No licenses available",
                    "unavailable_str": "\n".join(
                        f"{lic['name']} ({lic['reason']})" 
                        for lic in unavailable_licenses
                    ) if unavailable_licenses else "No unavailable licenses"
                }
                    
        except Exception as e:
            self.logger.error(f"License copy failed: {str(e)}", exc_info=True)
            results["licenses"] = self._empty_license_result()
        
    async def _copy_roles(self, source_id: str, target_id: str, 
                        results: Dict[str, Any]) -> None:
        """Copy roles from source to target user."""
        try:
            # Get source user's roles
            source_roles = await self._get_user_roles(source_id)
            if not source_roles:
                return

            for role in source_roles:
                try:
                    role_name = role.get('displayName', 'Unknown Role')
                    success = await self._assign_role_to_user(target_id, role['id'])
                    
                    if success:
                        results["roles"]["successful"].append(role_name)
                        results["copied_properties"].append(f"Role: {role_name}")
                    else:
                        results["roles"]["failed"].append(f"{role_name} (failed)")
                        
                except Exception as e:
                    self.logger.error(f"Failed to copy role {role_name}: {e}")
                    results["roles"]["failed"].append(
                        f"{role_name} (error: {str(e)})"
                    )
                    
        except Exception as e:
            self.logger.error(f"Role copy failed: {str(e)}")

    # D
    async def _diagnostic_license_check(self, user_id: str):
        """Diagnostic method to verify license state."""
        try:
            # Get user's current licenses
            current_licenses = await self._get_user_licenses(user_id)
            self.logger.debug(f"Current licenses for user {user_id}:")
            self.logger.debug(json.dumps(current_licenses, indent=2))

            # Get tenant SKUs
            tenant_skus = await self._get_tenant_skus()
            self.logger.debug("Available tenant SKUs:")
            self.logger.debug(json.dumps(tenant_skus, indent=2))

            return current_licenses, tenant_skus
        except Exception as e:
            self.logger.error(f"Diagnostic check failed: {str(e)}")
            return None, None
     
    # E
    def _empty_license_result(self) -> Dict[str, Any]:
        return {
            "available": [],
            "unavailable": [],
            "available_str": "",
            "unavailable_str": ""
        }
        
    def _empty_roles_result(self) -> Dict[str, List[str]]:
        """Initialize empty roles result structure."""
        return {
            "successful": [],
            "failed": []
        }
 
    # F
    def _failed_license_result(self, requested_licenses: Set[str]) -> Dict[str, Any]:
        return {
            "available": [],
            "unavailable": list(requested_licenses),
            "available_str": "",
            "unavailable_str": "License assignment failed"
        }

    def _find_best_user_match(self, users: List[Dict], search_term: str) -> Optional[Dict]:
        """Find best matching user using fuzzy matching."""
        name_map = {u['displayName']: u for u in users}
        if matches := get_close_matches(search_term, list(name_map.keys()), n=1, cutoff=0.8):
            return name_map[matches[0]]
        return None if not users else users[0]

    def _format_phone_number(self, phone_number: str) -> str:
        """Format phone number with extension support."""
        if not phone_number:
            return ""

        # Extract extension if present
        extension = ""
        for ext_marker in ['x', 'ext', 'ext.', 'extension']:
            if ext_marker in phone_number.lower():
                base, *ext_parts = phone_number.lower().split(ext_marker)
                phone_number = base
                if ext_parts:
                    extension = ext_parts[0].strip(' .')
                break

        # Clean and format main number
        digits = ''.join(c for c in phone_number if c.isdigit() or c == '+')
        
        if not digits.startswith('+'):
            digits = '+1' + digits if len(digits) == 10 else '+' + digits

        # Format based on number type
        if digits.startswith('+1'):
            formatted = f"{digits[:2]} ({digits[2:5]}) {digits[5:8]}-{digits[8:12]}"
            return f"{formatted} x{extension}" if extension else formatted
        else:
            formatted = digits
            return f"{formatted};ext={extension}" if extension else formatted

    def _format_final_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Format final result into a cleaner, organized structure."""
        from datetime import datetime
        return {
            "user": {
                "id": result["id"],
                "display_name": result["displayName"],
                "email": result["email"],
                "credentials": {
                    "initial_password": result["password"],
                    "password_link": result["password_link"]
                }
            },
            "memberships": {
                "groups": {
                    "added": result["groups"]["successful"],
                    "failed": result["groups"]["failed"],
                    "summary": f"Successfully added to {len(result['groups']['successful'])} groups"
                },
                "roles": {
                    "assigned": result["roles"]["successful"],
                    "failed": result["roles"]["failed"],
                    "summary": f"Successfully assigned {len(result['roles']['successful'])} roles"
                }
            },
            "licenses": {
                "assigned": {
                    "successful": [lic['friendlyName'] for lic in result["licenses"]["available"]],
                    "failed": result["licenses"]["unavailable"],
                    "available_details": result["licenses"]["available_str"],
                    "unavailable_details": result["licenses"]["unavailable_str"]
                }
            },
            "source_user": {
                "copied_from": result.get("copied_from", None),
                "copied_properties": result.get("copied_properties", [])
            },
            "status": {
                "success": True,
                "timestamp": datetime.now().isoformat(),
                "message": "User creation completed successfully"
            }
        }

    def _format_license_results(self, processed_licenses: list[Dict[str, Any]], 
                                tenant_skus: list[Dict[str, Any]]) -> Dict[str, Any]:
        """Format the results of license processing into a standardized output."""
        available = []
        unavailable = set()
        available_str_list = set()
        unavailable_str_list = set()
        
        for license_result in processed_licenses:
            if not license_result:  # Handle None results
                continue
                
            resolved_name = license_result.get('resolved_to', 'Unknown License')
            
            if license_result['matched']:
                sku_id = license_result['sku_id']
                # **Case-Insensitive Matching**
                matching_sku = next(
                    (sku for sku in tenant_skus if sku['skuId'].lower() == sku_id.lower()),
                    None
                )
                
                if matching_sku and matching_sku['remaining'] > 0:
                    available.append(matching_sku)
                    available_str_list.add(
                        f"{matching_sku['friendlyName']} ({matching_sku['remaining']} available)"
                    )
                else:
                    unavailable.add(resolved_name)
                    unavailable_str_list.add(
                        f"{resolved_name} (no licenses available)"
                    )
            else:
                unavailable.add(resolved_name)
                # Get specific reason for unavailability
                reason = {
                    'not_in_tenant': 'license not available in tenant',
                    'unknown_license': 'unknown license',
                    'invalid': 'invalid license format',
                    'error': 'processing error'
                }.get(license_result['type'], 'license unavailable')
                
                unavailable_str_list.add(
                    f"{resolved_name} ({reason})"
                )
        
        return {
            'available': available,
            'unavailable': list(unavailable),
            'available_str': "\n".join(sorted(available_str_list)) if available_str_list else "No licenses available",
            'unavailable_str': "\n".join(sorted(unavailable_str_list)) if unavailable_str_list else "No unavailable licenses"
        }

    # G
    async def _get_user_details(self, user_identifier: str) -> Optional[Dict[str, Any]]:
        """Get user details with caching support."""
        cache_key = f"user_details_{user_identifier.lower()}"
        if cached_user := self.cache_manager.get(cache_key):
            return cached_user

        try:
            # Optimize query with specific fields
            params = {
                "$select": "id,displayName,userPrincipalName",
                "$filter": (f"userPrincipalName eq '{user_identifier}'" if '@' in user_identifier
                          else f"startswith(displayName, '{user_identifier}')")
            }

            response = await self.request_manager.make_request(
                "GET", "users", params=params
            )
            users = response.json().get('value', [])

            if not users:
                return None

            # For email lookups, prefer exact match
            if '@' in user_identifier:
                user = next(
                    (u for u in users if u['userPrincipalName'].lower() == user_identifier.lower()),
                    users[0]
                )
            else:
                # For name lookups, use fuzzy matching
                user = self._find_best_user_match(users, user_identifier)

            if user:
                self.cache_manager.set(cache_key, user)
                return user

            return None

        except Exception as e:
            self.logger.error(f"Failed to get user details: {e}")
            return None

    async def _get_group_by_name(self, group_name: str) -> Optional[Dict[str, Any]]:
        """Get group details with caching and fuzzy matching."""
        cache_key = f"group_{group_name.lower()}"
        if cached_group := self.cache_manager.get(cache_key):
            return cached_group

        try:
            params = {
                "$select": "id,displayName",
                "$filter": f"startswith(displayName, '{group_name}')"
            }

            response = await self.request_manager.make_request(
                "GET", "groups", params=params
            )
            groups = response.json().get('value', [])

            if not groups:
                return None

            # Try exact match first
            if exact_match := next(
                (g for g in groups if g['displayName'].lower() == group_name.lower()),
                None
            ):
                self.cache_manager.set(cache_key, exact_match)
                return exact_match

            # Fall back to fuzzy matching
            group_map = {g['displayName']: g for g in groups}
            if matches := get_close_matches(group_name, list(group_map.keys()), n=1, cutoff=0.8):
                matched_group = group_map[matches[0]]
                self.cache_manager.set(cache_key, matched_group)
                return matched_group

            return None

        except Exception as e:
            self.logger.error(f"Failed to get group details: {e}")
            return None

    async def _get_user_licenses(self, user_id: str) -> List[Dict[str, str]]:
        """Get user's current licenses with debug logging."""
        try:
            response = await self.request_manager.make_request(
                "GET",
                f"users/{user_id}/licenseDetails"
            )
            raw_response = response.json()
            self.logger.debug(f"Raw license response: {json.dumps(raw_response, indent=2)}")
            
            return response.json().get('value', [])
        except Exception as e:
            self.logger.error(f"License fetch failed: {str(e)}")
            return []
      
    async def _get_tenant_skus(self) -> List[Dict[str, Any]]:
        """Get SKUs with caching."""
        cache_key = 'tenant_skus'
        if cached_skus := self.cache_manager.get(cache_key):
            return cached_skus

        try:
            response = await self.request_manager.make_request("GET", "subscribedSkus")
            tenant_skus = response.json().get('value', [])
            
            processed_skus = self._process_tenant_skus(tenant_skus)
            self.cache_manager.set(cache_key, processed_skus)
            
            return processed_skus

        except Exception as e:
            self.logger.error(f"Failed to get tenant SKUs: {e}")
            raise CacheError(f"Failed to fetch and cache tenant SKUs: {e}")

    async def _get_role_by_name(self, role_name: str) -> Optional[Dict[str, Any]]:
        """Retrieve role details by name."""
        try:
            params = {
                "$filter": f"displayName eq '{role_name}'",
                "$select": "id,displayName"
            }
            response = await self.request_manager.make_request(
                "GET",
                "directoryRoles",
                params=params
            )
            roles = response.json().get('value', [])
            if roles:
                return roles[0]
            return None
        except Exception as e:
            self.logger.error(f"Failed to retrieve role '{role_name}': {e}")
            return None

    async def _get_user_roles(self, user_id: str) -> List[Dict[str, Any]]:
        """Retrieve all directory roles assigned to a user."""
        try:
            # Define the endpoint and query parameters separately
            endpoint = f"users/{user_id}/memberOf/microsoft.graph.directoryRole"
            params = {
                "$select": "id,displayName"
            }

            response = await self.request_manager.make_request(
                "GET",
                endpoint,
                params=params
            )
            data = response.json()
            roles = data.get('value', [])
            processed_roles = [{'id': role['id'], 'displayName': role['displayName']} for role in roles]
            self.logger.debug(f"User {user_id} has roles: {processed_roles}")
            return processed_roles
        except Exception as e:
            self.logger.error(f"Failed to retrieve roles for user {user_id}: {e}")
            if hasattr(e, 'response') and e.response:
                try:
                    error_details = e.response.json()
                    self.logger.error(f"Error response: {json.dumps(error_details, indent=2)}")
                except Exception:
                    self.logger.error("No detailed error response available.")
            return []

    # H
    async def _handle_user_copying(self, target_user_id: str, 
                                source_user_identifier: str,
                                copy_licenses: bool = False,
                                skip_roles: bool = False) -> Dict[str, Any]:
        """Copy properties, memberships, and licenses from source to target user."""
        results = {
            "groups": {"successful": [], "failed": []},
            "licenses": self._empty_license_result(),
            "roles": {"successful": [], "failed": []},
            "copied_from": source_user_identifier,
            "copied_properties": []
        }

        try:
            source_user = await self._get_user_details(source_user_identifier)
            if not source_user:
                self.logger.error(f"Source user not found: {source_user_identifier}")
                return results

            self.logger.info(f"Copying from user: {source_user.get('displayName')}")
            results["copied_from"] = source_user.get('displayName')

            # Copy groups
            await self._copy_group_memberships(source_user['id'], target_user_id, results)

            # Copy licenses if requested
            if copy_licenses:
                await self._copy_licenses(source_user['id'], target_user_id, results)

            # Copy roles if not skipping
            if not skip_roles:
                await self._copy_roles(source_user['id'], target_user_id, results)

            return results

        except Exception as e:
            self.logger.error(f"User copy process failed: {str(e)}", exc_info=True)
            return results
      
    # I
    async def _initialize_user(self, display_name: str, email_address: str, 
                            kwargs: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Initialize user with required properties and complete structure."""
        try:
            # Create base user first
            user_result = await self.create_base_user(
                display_name=display_name,
                email_address=email_address,
                password=kwargs.get('password')
            )
            
            if not user_result:
                self.logger.error("Base user creation failed.")
                return None
                
            # Initialize complete result structure
            user_result.update({
                'groups': {"successful": [], "failed": []},
                'licenses': self._empty_license_result(),
                'roles': self._empty_roles_result(),
                'copied_from': None,
                'copied_properties': [],
                'password_link': await self._create_password_link(user_result['password'])
            })
            
            return user_result
            
        except Exception as e:
            self.logger.error(f"User initialization failed: {e}", exc_info=True)
            return None

    # M
    def _merge_template_results(self, user_result: Dict[str, Any], 
                            template_results: Dict[str, Any]) -> None:
        """Merge template user results into main result."""
        try:
            # Merge groups and licenses
            for category in ['groups', 'licenses']:
                self._merge_results(user_result, template_results, category)
            
            # Update template information
            user_result['copied_from'] = template_results.get('copied_from')
            user_result['copied_properties'].extend(
                template_results.get('copied_properties', [])
            )
            
        except Exception as e:
            self.logger.error(f"Failed to merge template results: {e}")

    def _merge_results(self, target: Dict[str, Any], source: Dict[str, Any], category: str) -> None:
        """Merge results while maintaining required structure."""
        try:
            if category == 'licenses':
                # Ensure license structure exists
                if 'licenses' not in target:
                    target['licenses'] = self._empty_license_result()

                # Merge license information
                target['licenses']['available'].extend(source.get('licenses', {}).get('available', []))
                target['licenses']['unavailable'].extend(source.get('licenses', {}).get('unavailable', []))
                
                # Update status strings
                if source.get('licenses', {}).get('available_str'):
                    if target['licenses']['available_str']:
                        target['licenses']['available_str'] += "\n" + source['licenses']['available_str']
                    else:
                        target['licenses']['available_str'] = source['licenses']['available_str']
                        
                if source.get('licenses', {}).get('unavailable_str'):
                    if target['licenses']['unavailable_str']:
                        target['licenses']['unavailable_str'] += "\n" + source['licenses']['unavailable_str']
                    else:
                        target['licenses']['unavailable_str'] = source['licenses']['unavailable_str']
            else:
                # Ensure category structure exists
                if category not in target:
                    target[category] = {"successful": [], "failed": []}

                # Merge lists
                target[category]['successful'].extend(source.get(category, {}).get('successful', []))
                target[category]['failed'].extend(source.get(category, {}).get('failed', []))

        except Exception as e:
            self.logger.error(f"Error merging results for {category}: {e}")

    def _merge_license_results(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        """Merge license results while preserving both copied and manual assignments."""
        try:
            # Track existing licenses to avoid duplicates
            existing_licenses = {
                lic['skuId'].lower() for lic in target['available']
            }
            
            # Add new available licenses while avoiding duplicates
            target['available'].extend(
                lic for lic in source.get('available', [])
                if lic['skuId'].lower() not in existing_licenses
            )
            
            # Merge unavailable licenses
            target['unavailable'].extend(source.get('unavailable', []))
            
            # Update available string
            if source.get('available_str'):
                if target['available_str'] and target['available_str'] != "No licenses available":
                    target['available_str'] += "\n" + source['available_str']
                else:
                    target['available_str'] = source['available_str']
                    
            # Update unavailable string
            if source.get('unavailable_str') and source['unavailable_str'] != "No unavailable licenses":
                if target['unavailable_str'] and target['unavailable_str'] != "No unavailable licenses":
                    target['unavailable_str'] += "\n" + source['unavailable_str']
                else:
                    target['unavailable_str'] = source['unavailable_str']
                    
        except Exception as e:
            self.logger.error(f"Error merging license results: {e}")
        
    # N
    def _normalize_license_list(self, licenses: Union[str, List[str], Set[str]]) -> Set[str]:
        """Normalize license input to a set of strings."""
        if isinstance(licenses, str):
            return {lic.strip() for lic in licenses.split(',') if lic.strip()}
        return set(licenses)

    def _normalize_group_list(self, groups: Union[str, List[str]]) -> List[str]:
        """Normalize group input to a list of strings."""
        if isinstance(groups, str):
            return [g.strip() for g in groups.split(',') if g.strip()]
        return list(groups)
   
    def _normalize_role_list(self, roles: Union[str, List[str]]) -> List[str]:
        """Normalize role input to a list of strings."""
        if isinstance(roles, str):
            return [r.strip() for r in roles.split(',') if r.strip()]
        return list(roles)

    # P
    def _process_tenant_skus(self, raw_skus: List[Dict]) -> List[Dict[str, Any]]:
        """Process raw SKU data into standardized format."""
        processed_skus = []
        for sku in raw_skus:
            sku_id = sku['skuId'].lower()
            sku_part_number = sku['skuPartNumber'].upper()
            
            friendly_name = next(
                (info["ProductName"] for info in self.product_licenses
                if info["StringID"].upper() == sku_part_number),
                sku_part_number
            )
            
            remaining = sku['prepaidUnits']['enabled'] - sku['consumedUnits']
            
            processed_skus.append({
                'skuId': sku_id,
                'skuPartNumber': sku_part_number,
                'friendlyName': friendly_name,
                'remaining': remaining,
                'enabled': sku['prepaidUnits']['enabled'],
                'consumed': sku['consumedUnits']
            })
            
        return processed_skus

    async def _process_license_request(self, requested_license: str,
                                tenant_skus: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process single license request with improved matching."""
        self.logger.info(f"Processing license request: {requested_license}")
        self.logger.info(f"Available tenant SKUs: {json.dumps(tenant_skus, indent=2)}")

        if not isinstance(requested_license, str):
            self.logger.warning(f"Invalid license format: {requested_license}")
            return self._invalid_license_result(requested_license)

        requested_license = requested_license.strip()
        self.logger.info(f"Available product licenses: {json.dumps(self.product_licenses, indent=2)}")
        
        # Try exact match first
        for license_info in self.product_licenses:
            if (license_info["StringID"].upper() == requested_license.upper() or
                license_info["ProductName"].upper() == requested_license.upper()):
                return await self._resolve_license_match(license_info, tenant_skus)

        # Try fuzzy matching
        product_names = [info["ProductName"] for info in self.product_licenses]
        if closest_matches := get_close_matches(requested_license, product_names, n=1, cutoff=0.75):
            matching_license = next(
                info for info in self.product_licenses
                if info["ProductName"] == closest_matches[0]
            )
            return await self._resolve_license_match(matching_license, tenant_skus)

        return self._unknown_license_result(requested_license)

    async def _process_all_roles(self, user_result: Dict[str, Any], 
                            kwargs: Dict[str, Any]) -> None:
        """Process all role assignments as the final step."""
        try:
            # First handle template roles if copying from template
            if template_user := kwargs.get('user_to_copy'):
                template_source = await self._get_user_details(template_user)
                if template_source:
                    template_roles = await self._get_user_roles(template_source['id'])
                    if template_roles:
                        for role in template_roles:
                            role_result = await self._assign_role_to_user(
                                user_result['id'], 
                                role['id']
                            )
                            if role_result:
                                user_result['roles']['successful'].append(
                                    f"{role['displayName']} (copied from user: {template_user})"
                                )
                                user_result['copied_properties'].append(
                                    f"Role: {role['displayName']}"
                                )
                            else:
                                user_result['roles']['failed'].append(
                                    f"{role['displayName']} (template copy failed)"
                                )

            # Then handle direct role assignments
            if roles := kwargs.get('roles'):
                role_results = await self.assign_roles(
                    user_result['id'],
                    self._normalize_role_list(roles)
                )
                self._merge_results(user_result, role_results, 'roles')

        except Exception as e:
            self.logger.error(f"Role processing failed: {str(e)}", exc_info=True)

    async def _process_template_user(self, user_result: Dict[str, Any], 
                                template_user: str, copy_licenses: bool,
                                skip_roles: bool = False) -> None:
        """Process template user copying excluding roles if specified."""
        try:
            copy_results = await self._handle_user_copying(
                user_result['id'],
                template_user,
                copy_licenses,
                skip_roles=skip_roles
            )
            
            if copy_results:
                self._merge_results(user_result, copy_results, 'groups')
                self._merge_results(user_result, copy_results, 'licenses')
                
                # Only merge roles if not skipping
                if not skip_roles:
                    self._merge_results(user_result, copy_results, 'roles')
                    
                # Update template information
                user_result['copied_from'] = copy_results.get('copied_from')
                user_result['copied_properties'].extend(
                    copy_results.get('copied_properties', [])
                )
                
        except Exception as e:
            self.logger.error(f"Template processing failed: {str(e)}", exc_info=True)

    async def _process_direct_assignments(self, user_result: Dict[str, Any], 
                                        kwargs: Dict[str, Any],
                                        skip_roles: bool = False) -> None:
        """Process direct assignments with enhanced tracking of manual vs copied items."""
        try:
            # Update user properties
            await self._update_user_properties(user_result['id'], kwargs)
            
            # Handle license assignments
            if license_skus := kwargs.get('license_skus'):
                normalized_licenses = self._normalize_license_list(license_skus)
                self.logger.debug(f"Processing direct license assignments: {normalized_licenses}")
                
                # Get current licenses structure
                current_licenses = user_result.get('licenses', self._empty_license_result())
                
                # Track which licenses were already assigned via template
                existing_licenses = {
                    lic['skuPartNumber'] for lic in current_licenses.get('available', [])
                }
                
                # Process new licenses
                license_results = await self.assign_licenses(
                    user_result['id'],
                    normalized_licenses
                )
                
                # Add manual assignment note for copied_properties
                for lic in license_results.get('available', []):
                    if lic['skuPartNumber'] not in existing_licenses:
                        user_result['copied_properties'].append(
                            f"License: {lic['friendlyName']} (manually assigned)"
                        )
                
                # Merge results
                self._merge_license_results(user_result['licenses'], license_results)
            
            # Handle group assignments
            if groups := kwargs.get('groups'):
                group_list = self._normalize_group_list(groups)
                
                # Track existing groups
                existing_groups = {
                    g.lower() for g in user_result['groups']['successful']
                }
                
                group_results = await self._add_user_to_groups(
                    user_result['id'],
                    group_list
                )
                
                # Add manual assignment note for new groups
                for group in group_results['successful']:
                    clean_group_name = group.split(" (already")[0]  # Remove any suffix
                    if clean_group_name.lower() not in existing_groups:
                        user_result['copied_properties'].append(
                            f"Group: {clean_group_name} (manually assigned)"
                        )
                
                self._merge_results(user_result, {'groups': group_results}, 'groups')
            
            # Handle roles only if not skipping
            if not skip_roles and kwargs.get('roles'):
                role_results = await self.assign_roles(
                    user_result['id'],
                    self._normalize_role_list(kwargs['roles'])
                )
                self._merge_results(user_result, {'roles': role_results}, 'roles')
                    
        except Exception as e:
            self.logger.error(f"Direct assignments failed: {str(e)}", exc_info=True)

    # R
    async def _resolve_license_match(self, license_info: Dict[str, str], 
                                tenant_skus: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Resolve license match against tenant SKUs."""
        try:
            matching_sku = next(
                (sku for sku in tenant_skus 
                if sku['skuPartNumber'].upper() == license_info["StringID"].upper()),
                None
            )
            
            if matching_sku:
                self.logger.debug(f"Found matching SKU: {matching_sku['friendlyName']}")
                return {
                    'matched': True,
                    'type': 'exact_match',
                    'resolved_to': matching_sku['friendlyName'],
                    'sku_id': matching_sku['skuId'],
                    'remaining': matching_sku.get('remaining', 0)
                }
            
            self.logger.debug(f"License {license_info['ProductName']} not available in tenant")
            return {
                'matched': False,
                'type': 'not_in_tenant',
                'resolved_to': license_info['ProductName'],
                'remaining': 0
            }
        except Exception as e:
            self.logger.error(f"Error resolving license match: {e}")
            return {
                'matched': False,
                'type': 'error',
                'resolved_to': license_info.get('ProductName', 'Unknown'),
                'remaining': 0
            }

    # S
    def _split_display_name(self, display_name: str) -> Tuple[str, str]:
        """Split display name into first and last names."""
        parts = display_name.split(" ", 1)
        return parts[0], parts[1] if len(parts) > 1 else ""

    # U
    async def _update_user_properties(self, user_id: str, 
                                    properties: Dict[str, Any]) -> None:
        """Update user properties with validation."""
        update_payload = {}
        
        # Handle phone numbers
        if business_phone := properties.get('business_phone'):
            formatted_phone = self._format_phone_number(business_phone)
            self.logger.debug(f"[{user_id}] Formatted business phone: {formatted_phone}")
            update_payload['businessPhones'] = [formatted_phone]
        else:
            self.logger.debug(f"[{user_id}] No business phone provided.")
            
        if mobile_phone := properties.get('mobile_phone'):
            formatted_mobile = self._format_phone_number(mobile_phone)
            self.logger.debug(f"[{user_id}] Formatted mobile phone: {formatted_mobile}")
            update_payload['mobilePhone'] = formatted_mobile
        else:
            self.logger.debug(f"[{user_id}] No mobile phone provided.")

        # Handle other properties
        property_mapping = {
            'job_title': 'jobTitle',
            'department': 'department',
            'office_location': 'officeLocation',
            'city': 'city',
            'state': 'state'
        }

        for source_key, target_key in property_mapping.items():
            if value := properties.get(source_key):
                self.logger.debug(f"[{user_id}] Mapping '{source_key}' to '{target_key}' with value: {value}")
                update_payload[target_key] = value
            else:
                self.logger.debug(f"[{user_id}] No value provided for '{source_key}'.")

        if update_payload:
            self.logger.info(f"[{user_id}] Updating user properties with payload: {json.dumps(update_payload, indent=2)}")
            try:
                response = await self.request_manager.make_request(
                    "PATCH",
                    f"users/{user_id}",
                    json_data=update_payload
                )
                
                # Log the response status and body
                self.logger.debug(f"[{user_id}] Received response status: {response.status_code}")
                try:
                    response_body = response.json()
                    self.logger.debug(f"[{user_id}] Received response body: {json.dumps(response_body, indent=2)}")
                except json.JSONDecodeError:
                    response_body = response.text
                    self.logger.debug(f"[{user_id}] Received non-JSON response body: {response_body}")
                
                if response.status_code >= 400:
                    self.logger.error(f"[{user_id}] Failed to update user properties. Status: {response.status_code}, Body: {response_body}")
                    raise InsufficientPermissionsError(f"Failed to update user properties for user '{user_id}'. Status Code: {response.status_code}")
                else:
                    self.logger.info(f"[{user_id}] Successfully updated user properties.")
                    
            except InsufficientPermissionsError as e:
                self.logger.error(f"[{user_id}] Insufficient permissions error: {e}", exc_info=True)
                raise
            except Exception as e:
                self.logger.error(f"[{user_id}] Unexpected error during user property update: {e}", exc_info=True)
                raise
        else:
            self.logger.info(f"[{user_id}] No properties to update.")

    # V
    @staticmethod
    def _validate_email(email: str) -> bool:
        """Validate email format."""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'


        return bool(re.match(pattern, email))

    def _validate_result(self, result: Dict[str, Any]) -> bool:
        """Validate the structure of the user creation result."""
        try:
            required_fields = {
                'user': ['id', 'display_name', 'email', 'credentials'],
                'user.credentials': ['initial_password', 'password_link'],
                'memberships': ['groups', 'roles'],
                'licenses': ['assigned'],
                'status': ['success', 'timestamp', 'message']
            }

            # Check top-level structure
            if not all(field in result for field in required_fields):
                return False

            # Check user section
            user = result.get('user', {})
            if not all(field in user for field in required_fields['user']):
                return False

            # Check credentials
            credentials = user.get('credentials', {})
            if not all(field in credentials for field in required_fields['user.credentials']):
                return False

            return True

        except Exception as e:
            self.logger.error(f"Result validation failed: {e}")
            return False






    

