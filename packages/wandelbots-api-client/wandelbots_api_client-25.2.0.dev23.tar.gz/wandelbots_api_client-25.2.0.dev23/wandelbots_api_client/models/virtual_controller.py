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

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from wandelbots_api_client.models.manufacturer import Manufacturer
from wandelbots_api_client.models.virtual_controller_types import VirtualControllerTypes
from typing import Optional, Set
from typing_extensions import Self

class VirtualController(BaseModel):
    """
    The configuration of a virtual robot controller has to contain the manufacturer string, an optional joint position string array and either a type or the full JSON configuration. The JSON config of a physical controller can be obtained via `/cells/{cell}/controllers/{controller}/virtual-robot-configuration` 
    """ # noqa: E501
    kind: Optional[StrictStr] = 'VirtualController'
    manufacturer: Manufacturer
    type: Optional[VirtualControllerTypes] = None
    var_json: Optional[StrictStr] = Field(default=None, alias="json")
    position: Optional[StrictStr] = Field(default=None, description="Initial joint position of the first motion group from the virtual robot controller. Provide the joint position as a JSON array containing 7 float values, each representing a joint position in radians, e.g. \"[0, 0, 0, 0, 0, 0, 0]\". If the robot has fewer than 7 joints, use \"0\" for each remaining position to ensure the array has exactly 7 values. ")
    __properties: ClassVar[List[str]] = ["kind", "manufacturer", "type", "json", "position"]

    @field_validator('kind')
    def kind_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['VirtualController']):
            raise ValueError("must be one of enum values ('VirtualController')")
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
        """Create an instance of VirtualController from a JSON string"""
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
        """Create an instance of VirtualController from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "kind": obj.get("kind") if obj.get("kind") is not None else 'VirtualController',
            "manufacturer": obj.get("manufacturer"),
            "type": obj.get("type"),
            "json": obj.get("json"),
            "position": obj.get("position")
        })
        return _obj


