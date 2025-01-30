# coding: utf-8

"""
    Wandelbots Nova API

    Interact with robots in an easy and intuitive way.  > **Note:** API version 2 is experimental and will experience functional changes. 

    The version of the OpenAPI document: 2.0.0 beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from wandelbots_api_client.v2.models.motion_group_state import MotionGroupState
from wandelbots_api_client.v2.models.operation_mode import OperationMode
from wandelbots_api_client.v2.models.safety_state_type import SafetyStateType
from typing import Optional, Set
from typing_extensions import Self

class RobotControllerState(BaseModel):
    """
    Returns the whole current state of robot controller.
    """ # noqa: E501
    controller: StrictStr = Field(description="Identifier of the configured robot controller.")
    operation_mode: OperationMode
    safety_state: SafetyStateType
    timestamp: datetime = Field(description="Timestamp indicating when the represented information was received from the robot controller.")
    velocity_override: Optional[StrictInt] = Field(default=None, description="If made available by the robot controller, returns the current velocity override in [percentage] for movements adjusted on robot control panel. Valid value range: 1 - 100. ")
    active_motion_groups: List[MotionGroupState] = Field(description="State of indicated motion groups. In case of state request via controller all configured motion groups are returned. In case of executing a motion only the affected motion groups are returned. ")
    __properties: ClassVar[List[str]] = ["controller", "operation_mode", "safety_state", "timestamp", "velocity_override", "active_motion_groups"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of RobotControllerState from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each item in active_motion_groups (list)
        _items = []
        if self.active_motion_groups:
            for _item in self.active_motion_groups:
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to not drop empty elements in lists
                if _item is not None:
                    _items.append(_item.to_dict())
                # <<< End modification
            _dict['active_motion_groups'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RobotControllerState from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "controller": obj.get("controller") if obj.get("controller") is not None else 'controller',
            "operation_mode": obj.get("operation_mode"),
            "safety_state": obj.get("safety_state"),
            "timestamp": obj.get("timestamp"),
            "velocity_override": obj.get("velocity_override"),
            "active_motion_groups": [
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to allow dicts in lists
                MotionGroupState.from_dict(_item) if hasattr(MotionGroupState, 'from_dict') else _item
                # <<< End modification
                for _item in obj["active_motion_groups"]
            ] if obj.get("active_motion_groups") is not None else None
        })
        return _obj


