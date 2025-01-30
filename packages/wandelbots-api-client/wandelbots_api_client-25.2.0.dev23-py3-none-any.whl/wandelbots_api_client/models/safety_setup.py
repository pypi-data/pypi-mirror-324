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

from pydantic import BaseModel, ConfigDict
from typing import Any, ClassVar, Dict, List, Optional
from wandelbots_api_client.models.robot_link_geometry import RobotLinkGeometry
from wandelbots_api_client.models.safety_setup_safety_settings import SafetySetupSafetySettings
from wandelbots_api_client.models.safety_setup_safety_zone import SafetySetupSafetyZone
from wandelbots_api_client.models.tool_geometry import ToolGeometry
from typing import Optional, Set
from typing_extensions import Self

class SafetySetup(BaseModel):
    """
    SafetySetup
    """ # noqa: E501
    safety_settings: Optional[List[SafetySetupSafetySettings]] = None
    safety_zones: Optional[List[SafetySetupSafetyZone]] = None
    robot_model_geometries: Optional[List[RobotLinkGeometry]] = None
    tool_geometries: Optional[List[ToolGeometry]] = None
    __properties: ClassVar[List[str]] = ["safety_settings", "safety_zones", "robot_model_geometries", "tool_geometries"]

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
        """Create an instance of SafetySetup from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in safety_settings (list)
        _items = []
        if self.safety_settings:
            for _item in self.safety_settings:
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to not drop empty elements in lists
                if _item is not None:
                    _items.append(_item.to_dict())
                # <<< End modification
            _dict['safety_settings'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in safety_zones (list)
        _items = []
        if self.safety_zones:
            for _item in self.safety_zones:
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to not drop empty elements in lists
                if _item is not None:
                    _items.append(_item.to_dict())
                # <<< End modification
            _dict['safety_zones'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in robot_model_geometries (list)
        _items = []
        if self.robot_model_geometries:
            for _item in self.robot_model_geometries:
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to not drop empty elements in lists
                if _item is not None:
                    _items.append(_item.to_dict())
                # <<< End modification
            _dict['robot_model_geometries'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in tool_geometries (list)
        _items = []
        if self.tool_geometries:
            for _item in self.tool_geometries:
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to not drop empty elements in lists
                if _item is not None:
                    _items.append(_item.to_dict())
                # <<< End modification
            _dict['tool_geometries'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SafetySetup from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "safety_settings": [
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to allow dicts in lists
                SafetySetupSafetySettings.from_dict(_item) if hasattr(SafetySetupSafetySettings, 'from_dict') else _item
                # <<< End modification
                for _item in obj["safety_settings"]
            ] if obj.get("safety_settings") is not None else None,
            "safety_zones": [
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to allow dicts in lists
                SafetySetupSafetyZone.from_dict(_item) if hasattr(SafetySetupSafetyZone, 'from_dict') else _item
                # <<< End modification
                for _item in obj["safety_zones"]
            ] if obj.get("safety_zones") is not None else None,
            "robot_model_geometries": [
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to allow dicts in lists
                RobotLinkGeometry.from_dict(_item) if hasattr(RobotLinkGeometry, 'from_dict') else _item
                # <<< End modification
                for _item in obj["robot_model_geometries"]
            ] if obj.get("robot_model_geometries") is not None else None,
            "tool_geometries": [
                # >>> Modified from https://github.com/OpenAPITools/openapi-generator/blob/v7.6.0/modules/openapi-generator/src/main/resources/python/model_generic.mustache
                #     to allow dicts in lists
                ToolGeometry.from_dict(_item) if hasattr(ToolGeometry, 'from_dict') else _item
                # <<< End modification
                for _item in obj["tool_geometries"]
            ] if obj.get("tool_geometries") is not None else None
        })
        return _obj


