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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set
from typing_extensions import Self

class JointLimit(BaseModel):
    """
    A joint limit can contain a position (rad or mm), a velocity (rad/s or mm/s), an acceleration (rad/s² or mm/s²) or a jerk (rad/s³ or mm/s³). 
    """ # noqa: E501
    joint: StrictStr = Field(description="Definition of the joint where the limits are applied.")
    lower_limit: Union[StrictFloat, StrictInt] = Field(description="Lower joint limit which is smaller than the upper joint limit.")
    upper_limit: Union[StrictFloat, StrictInt] = Field(description="Upper joint boundary which is bigger than the lower joint limit.")
    unlimited: Optional[StrictBool] = Field(default=None, description="True, if joint limit is unlimited. Lower and upper limits are ignored.")
    __properties: ClassVar[List[str]] = ["joint", "lower_limit", "upper_limit", "unlimited"]

    @field_validator('joint')
    def joint_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['JOINTNAME_AXIS_INVALID', 'JOINTNAME_AXIS_1', 'JOINTNAME_AXIS_2', 'JOINTNAME_AXIS_3', 'JOINTNAME_AXIS_4', 'JOINTNAME_AXIS_5', 'JOINTNAME_AXIS_6', 'JOINTNAME_AXIS_7', 'JOINTNAME_AXIS_8', 'JOINTNAME_AXIS_9', 'JOINTNAME_AXIS_10', 'JOINTNAME_AXIS_11', 'JOINTNAME_AXIS_12']):
            raise ValueError("must be one of enum values ('JOINTNAME_AXIS_INVALID', 'JOINTNAME_AXIS_1', 'JOINTNAME_AXIS_2', 'JOINTNAME_AXIS_3', 'JOINTNAME_AXIS_4', 'JOINTNAME_AXIS_5', 'JOINTNAME_AXIS_6', 'JOINTNAME_AXIS_7', 'JOINTNAME_AXIS_8', 'JOINTNAME_AXIS_9', 'JOINTNAME_AXIS_10', 'JOINTNAME_AXIS_11', 'JOINTNAME_AXIS_12')")
        return value

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
        """Create an instance of JointLimit from a JSON string"""
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
        """Create an instance of JointLimit from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "joint": obj.get("joint"),
            "lower_limit": obj.get("lower_limit"),
            "upper_limit": obj.get("upper_limit"),
            "unlimited": obj.get("unlimited")
        })
        return _obj


