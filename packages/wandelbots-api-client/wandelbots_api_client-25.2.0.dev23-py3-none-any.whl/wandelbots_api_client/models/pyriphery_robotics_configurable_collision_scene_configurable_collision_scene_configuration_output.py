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
from typing import Any, ClassVar, Dict, List, Optional
from wandelbots_api_client.models.collider_output import ColliderOutput
from wandelbots_api_client.models.collision_robot_configuration_output import CollisionRobotConfigurationOutput
from typing import Optional, Set
from typing_extensions import Self

class PyripheryRoboticsConfigurableCollisionSceneConfigurableCollisionSceneConfigurationOutput(BaseModel):
    """
    PyripheryRoboticsConfigurableCollisionSceneConfigurableCollisionSceneConfigurationOutput
    """ # noqa: E501
    type: Optional[Any] = None
    identifier: Optional[StrictStr] = Field(default='scene', description="A unique identifier for the collision scene.")
    static_colliders: Optional[Dict[str, ColliderOutput]] = Field(default=None, description="A collection of static colliders within the scene, identified by their names.")
    robot_configurations: Optional[Dict[str, CollisionRobotConfigurationOutput]] = Field(default=None, description="Configurations for robots within the scene. Allow for the specification of collision geometries and other robot-specific settings, identified by robot names. ")
    __properties: ClassVar[List[str]] = ["type", "identifier", "static_colliders", "robot_configurations"]

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
        """Create an instance of PyripheryRoboticsConfigurableCollisionSceneConfigurableCollisionSceneConfigurationOutput from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each value in static_colliders (dict)
        _field_dict = {}
        if self.static_colliders:
            for _key in self.static_colliders:
                if self.static_colliders[_key]:
                    _field_dict[_key] = self.static_colliders[_key].to_dict()
            _dict['static_colliders'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of each value in robot_configurations (dict)
        _field_dict = {}
        if self.robot_configurations:
            for _key in self.robot_configurations:
                if self.robot_configurations[_key]:
                    _field_dict[_key] = self.robot_configurations[_key].to_dict()
            _dict['robot_configurations'] = _field_dict
        # set to None if type (nullable) is None
        # and model_fields_set contains the field
        if self.type is None and "type" in self.model_fields_set:
            _dict['type'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PyripheryRoboticsConfigurableCollisionSceneConfigurableCollisionSceneConfigurationOutput from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "identifier": obj.get("identifier") if obj.get("identifier") is not None else 'scene',
            "static_colliders": dict(
                (_k, ColliderOutput.from_dict(_v))
                for _k, _v in obj["static_colliders"].items()
            )
            if obj.get("static_colliders") is not None
            else None,
            "robot_configurations": dict(
                (_k, CollisionRobotConfigurationOutput.from_dict(_v))
                for _k, _v in obj["robot_configurations"].items()
            )
            if obj.get("robot_configurations") is not None
            else None
        })
        return _obj


