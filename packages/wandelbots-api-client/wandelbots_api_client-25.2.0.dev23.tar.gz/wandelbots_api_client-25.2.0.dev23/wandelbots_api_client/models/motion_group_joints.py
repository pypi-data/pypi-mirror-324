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

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set
from typing_extensions import Self

class MotionGroupJoints(BaseModel):
    """
    Ensure to provide one value for each joint. See [getMotionGroups](getMotionGroups) for the number of joints. Everything but positions is optional.
    """ # noqa: E501
    positions: List[Union[StrictFloat, StrictInt]] = Field(description="The joint positions of the motion group. ")
    velocities: Optional[List[Union[StrictFloat, StrictInt]]] = Field(default=None, description="The joint velocities of the motion group. ")
    accelerations: Optional[List[Union[StrictFloat, StrictInt]]] = Field(default=None, description="The joint accelerations of the motion group. ")
    torques: Optional[List[Union[StrictFloat, StrictInt]]] = Field(default=None, description="The joint torques of the motion group. ")
    __properties: ClassVar[List[str]] = ["positions", "velocities", "accelerations", "torques"]

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
        """Create an instance of MotionGroupJoints from a JSON string"""
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
        """Create an instance of MotionGroupJoints from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "positions": obj.get("positions"),
            "velocities": obj.get("velocities"),
            "accelerations": obj.get("accelerations"),
            "torques": obj.get("torques")
        })
        return _obj


