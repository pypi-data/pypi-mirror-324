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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List
from wandelbots_api_client.models.joints import Joints
from typing import Optional, Set
from typing_extensions import Self

class PlanSuccessfulResponse(BaseModel):
    """
    The motion can be executed entirely.
    """ # noqa: E501
    motion: StrictStr = Field(description="Unique identifier of the motion. Use as reference to execute the motion or to retrieve information on the motion.")
    end_joint_position: Joints = Field(description="The final joint position. Use this position as a start joint position to concatenate motions.")
    __properties: ClassVar[List[str]] = ["motion", "end_joint_position"]

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
        """Create an instance of PlanSuccessfulResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of end_joint_position
        if self.end_joint_position:
            _dict['end_joint_position'] = self.end_joint_position.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PlanSuccessfulResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "motion": obj.get("motion"),
            "end_joint_position": Joints.from_dict(obj["end_joint_position"]) if obj.get("end_joint_position") is not None else None
        })
        return _obj


