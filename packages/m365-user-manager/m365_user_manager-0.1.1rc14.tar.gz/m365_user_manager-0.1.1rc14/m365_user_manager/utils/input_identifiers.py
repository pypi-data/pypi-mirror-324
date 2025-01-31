#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ./m365_user_manager/utils/input_identifiers.py

from dataclasses import dataclass, field
from typing import Dict, Set, ClassVar

@dataclass
class FormFields:
    """
    Manages form field identifiers for M365 user management.
    """
    DISPLAY_NAME: str = field(default="DisplayName_1737154608192")
    EMAIL_ADDRESS: str = field(default="EmailAddress_1737154657850")
    PASSWORD: str = field(default="Password_1737154656469")
    JOB_TITLE: str = field(default="JobTitle_1737154733788")
    DEPARTMENT: str = field(default="Department_1737154731291")
    OFFICE_LOCATION: str = field(default="OfficeLocation_1737154659481")
    CITY: str = field(default="City_1737154742161")
    STATE: str = field(default="State_1737154743922")
    BUSINESS_PHONE: str = field(default="BusinessPhone_1737154735784")
    MOBILE_PHONE: str = field(default="MobilePhone_1737154737302")
    GROUPS: str = field(default="Groups_1737154746910")
    LICENSE_SKUS: str = field(default="LicenseSKUs_1737154745588")
    USER_TO_COPY: str = field(default="UserToCopy_1737154748715")
    COPY_LICENSES: str = field(default="CopyLicenses_1737159741637")
    PASSWORD_PUSH_TOKEN: str = field(default="PasswordPushToken_1737575340807")
    WEBHOOK_URL: str = field(default="Webhook_URL_1738104979016")
    WORKSTATION_SETUP: str = field(default="WorkstationSetup_1738104979016")

    # Field type mappings - use uppercase to match field names
    _required_fields: ClassVar[Set[str]] = {"DISPLAY_NAME", "EMAIL_ADDRESS"}
    _list_fields: ClassVar[Set[str]] = {"GROUPS", "LICENSE_SKUS"}
    _boolean_fields: ClassVar[Set[str]] = {"COPY_LICENSES"}

    def __init__(self, **kwargs):
        """Initialize with optional field overrides."""
        # Set defaults first
        self.__class__.__dataclass_fields__  # Ensure dataclass fields are created
        
        # Then override with any provided values
        field_map = {
            'webhook_url': 'WEBHOOK_URL',
            'display_name': 'DISPLAY_NAME',
            'email_address': 'EMAIL_ADDRESS',
            'password': 'PASSWORD',
            'job_title': 'JOB_TITLE',
            'department': 'DEPARTMENT',
            'office_location': 'OFFICE_LOCATION',
            'city': 'CITY',
            'state': 'STATE',
            'business_phone': 'BUSINESS_PHONE',
            'mobile_phone': 'MOBILE_PHONE',
            'groups': 'GROUPS',
            'license_skus': 'LICENSE_SKUS',
            'user_to_copy': 'USER_TO_COPY',
            'copy_licenses': 'COPY_LICENSES',
            'password_push_token': 'PASSWORD_PUSH_TOKEN',
            'workstation_setup': 'WORKSTATION_SETUP'
        }
        
        for key, value in kwargs.items():
            if key in field_map:
                setattr(self, field_map[key], value)

    @property
    def required_fields(self) -> Set[str]:
        """Get IDs of required fields."""
        return {getattr(self, field) for field in self._required_fields}

    @property
    def list_fields(self) -> Set[str]:
        """Get IDs of list fields."""
        return {getattr(self, field) for field in self._list_fields}

    @property
    def boolean_fields(self) -> Set[str]:
        """Get IDs of boolean fields."""
        return {getattr(self, field) for field in self._boolean_fields}

    def get_field_mapping(self) -> Dict[str, str]:
        """Get mapping of field names to their identifiers."""
        return {
            'display_name': self.DISPLAY_NAME,
            'email_address': self.EMAIL_ADDRESS,
            'password': self.PASSWORD,
            'job_title': self.JOB_TITLE,
            'department': self.DEPARTMENT,
            'office_location': self.OFFICE_LOCATION,
            'city': self.CITY,
            'state': self.STATE,
            'business_phone': self.BUSINESS_PHONE,
            'mobile_phone': self.MOBILE_PHONE,
            'groups': self.GROUPS,
            'license_skus': self.LICENSE_SKUS,
            'user_to_copy': self.USER_TO_COPY,
            'copy_licenses': self.COPY_LICENSES,
            'webhook_url': self.WEBHOOK_URL,
            'password_push_token': self.PASSWORD_PUSH_TOKEN,
            'workstation_setup': self.WORKSTATION_SETUP
        }

    def set_ids(self, **kwargs) -> None:
        """Set new IDs for form fields."""
        self.__init__(**kwargs)

    def get_ids(self) -> Dict[str, str]:
        """Get all current field IDs."""
        return {
            'display_name': self.DISPLAY_NAME,
            'email_address': self.EMAIL_ADDRESS,
            'password': self.PASSWORD,
            'job_title': self.JOB_TITLE,
            'department': self.DEPARTMENT,
            'office_location': self.OFFICE_LOCATION,
            'city': self.CITY,
            'state': self.STATE,
            'business_phone': self.BUSINESS_PHONE,
            'mobile_phone': self.MOBILE_PHONE,
            'groups': self.GROUPS,
            'license_skus': self.LICENSE_SKUS,
            'user_to_copy': self.USER_TO_COPY,
            'copy_licenses': self.COPY_LICENSES,
            'password_push_token': self.PASSWORD_PUSH_TOKEN,
            'webhook_url': self.WEBHOOK_URL,
            'workstation_setup': self.WORKSTATION_SETUP
        }