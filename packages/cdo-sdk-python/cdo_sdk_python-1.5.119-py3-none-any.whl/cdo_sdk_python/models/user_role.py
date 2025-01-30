# coding: utf-8

"""
    Cisco Security Cloud Control API

    Use the documentation to explore the endpoints Security Cloud Control has to offer

    The version of the OpenAPI document: 1.5.0
    Contact: cdo.tac@cisco.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class UserRole(str, Enum):
    """
    This determines the role for all the users included in this Active Directory Group.
    """

    """
    allowed enum values
    """
    ROLE_ADMIN = 'ROLE_ADMIN'
    ROLE_SUPER_ADMIN = 'ROLE_SUPER_ADMIN'
    ROLE_READ_ONLY = 'ROLE_READ_ONLY'
    ROLE_DEPLOY_ONLY = 'ROLE_DEPLOY_ONLY'
    ROLE_EDIT_ONLY = 'ROLE_EDIT_ONLY'
    ROLE_VPN_SESSIONS_MANAGER = 'ROLE_VPN_SESSIONS_MANAGER'
    ROLE_FWAAS = 'ROLE_FWAAS'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of UserRole from a JSON string"""
        return cls(json.loads(json_str))


