# coding: utf-8

"""
    Wandelbots Nova API

    Interact with robots in an easy and intuitive way. 

    The version of the OpenAPI document: 1.0.0 beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class MotionGroupPhysical(BaseModel):
    """
    The data type describes the physically connected motion groups on a robot controller. 
    """ # noqa: E501
    motion_group: StrictStr = Field(description="The unique identifier to address a motion group.")
    name_from_controller: StrictStr = Field(description="The name the motion group has on the robot controller.")
    active: StrictBool = Field(description="True if this motion group is active. When a request for a motion group is made, the motion group will be activated and remain activated. The robot controller provides the current state and data for all active motion groups. See [getCurrentMotionGroupState](getCurrentMotionGroupState). To deactivate a motion group, use [deactivateMotionGroup](deactivateMotionGroup). ")
    model_from_controller: Optional[StrictStr] = Field(default=None, description="The robot controller model if available. Usable for frontend 3D visualization.")
    serial_number: Optional[StrictStr] = Field(default=None, description="The serial number of the motion group if available. If not available, the serial number of the robot controller. if available. If not available, then empty. ")
    __properties: ClassVar[List[str]] = ["motion_group", "name_from_controller", "active", "model_from_controller", "serial_number"]

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
        """Create an instance of MotionGroupPhysical from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of MotionGroupPhysical from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "motion_group": obj.get("motion_group"),
            "name_from_controller": obj.get("name_from_controller"),
            "active": obj.get("active"),
            "model_from_controller": obj.get("model_from_controller"),
            "serial_number": obj.get("serial_number")
        })
        return _obj


