# coding: utf-8

"""
    Wandelbots Nova API

    Interact with robots in an easy and intuitive way.  > **Note:** API version 2 is experimental and will experience functional changes. 

    The version of the OpenAPI document: 2.0.0 beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class StandstillReason(str, Enum):
    """
    The reason why the movement is paused.
    """

    """
    allowed enum values
    """
    REASON_MOTION_ENDED = 'REASON_MOTION_ENDED'
    REASON_USER_PAUSED_MOTION = 'REASON_USER_PAUSED_MOTION'
    REASON_WAITING_FOR_IO = 'REASON_WAITING_FOR_IO'
    REASON_PAUSED_ON_IO = 'REASON_PAUSED_ON_IO'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of StandstillReason from a JSON string"""
        return cls(json.loads(json_str))


