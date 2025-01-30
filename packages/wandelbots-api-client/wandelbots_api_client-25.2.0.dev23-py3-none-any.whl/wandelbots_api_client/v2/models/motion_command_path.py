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
import pprint
from pydantic import BaseModel, ConfigDict, Field, StrictStr, ValidationError, field_validator
from typing import Any, List, Optional
from wandelbots_api_client.v2.models.path_cartesian_ptp import PathCartesianPTP
from wandelbots_api_client.v2.models.path_circle import PathCircle
from wandelbots_api_client.v2.models.path_cubic_spline import PathCubicSpline
from wandelbots_api_client.v2.models.path_joint_ptp import PathJointPTP
from wandelbots_api_client.v2.models.path_line import PathLine
from pydantic import StrictStr, Field
from typing import Union, List, Set, Optional, Dict
from typing_extensions import Literal, Self

MOTIONCOMMANDPATH_ONE_OF_SCHEMAS = ["PathCartesianPTP", "PathCircle", "PathCubicSpline", "PathJointPTP", "PathLine"]

class MotionCommandPath(BaseModel):
    """
    MotionCommandPath
    """
    # data type: PathCartesianPTP
    oneof_schema_1_validator: Optional[PathCartesianPTP] = None
    # data type: PathCubicSpline
    oneof_schema_2_validator: Optional[PathCubicSpline] = None
    # data type: PathLine
    oneof_schema_3_validator: Optional[PathLine] = None
    # data type: PathCircle
    oneof_schema_4_validator: Optional[PathCircle] = None
    # data type: PathJointPTP
    oneof_schema_5_validator: Optional[PathJointPTP] = None
    actual_instance: Optional[Union[PathCartesianPTP, PathCircle, PathCubicSpline, PathJointPTP, PathLine]] = None
    one_of_schemas: Set[str] = { "PathCartesianPTP", "PathCircle", "PathCubicSpline", "PathJointPTP", "PathLine" }

    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )


    discriminator_value_class_map: Dict[str, str] = {
    }

    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator('actual_instance')
    def actual_instance_must_validate_oneof(cls, v):
        instance = MotionCommandPath.model_construct()
        error_messages = []
        match = 0
        # validate data type: PathCartesianPTP
        if not isinstance(v, PathCartesianPTP):
            error_messages.append(f"Error! Input type `{type(v)}` is not `PathCartesianPTP`")
        else:
            match += 1
        # validate data type: PathCubicSpline
        if not isinstance(v, PathCubicSpline):
            error_messages.append(f"Error! Input type `{type(v)}` is not `PathCubicSpline`")
        else:
            match += 1
        # validate data type: PathLine
        if not isinstance(v, PathLine):
            error_messages.append(f"Error! Input type `{type(v)}` is not `PathLine`")
        else:
            match += 1
        # validate data type: PathCircle
        if not isinstance(v, PathCircle):
            error_messages.append(f"Error! Input type `{type(v)}` is not `PathCircle`")
        else:
            match += 1
        # validate data type: PathJointPTP
        if not isinstance(v, PathJointPTP):
            error_messages.append(f"Error! Input type `{type(v)}` is not `PathJointPTP`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in MotionCommandPath with oneOf schemas: PathCartesianPTP, PathCircle, PathCubicSpline, PathJointPTP, PathLine. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in MotionCommandPath with oneOf schemas: PathCartesianPTP, PathCircle, PathCubicSpline, PathJointPTP, PathLine. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Union[str, Dict[str, Any]]) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []
        match = 0

        # use oneOf discriminator to lookup the data type
        _data_type = json.loads(json_str).get("path_definition_name")
        if not _data_type:
            raise ValueError("Failed to lookup data type from the field `path_definition_name` in the input.")

        # check if data type is `PathCartesianPTP`
        if _data_type == "PathCartesianPTP":
            instance.actual_instance = PathCartesianPTP.from_json(json_str)
            return instance

        # check if data type is `PathCircle`
        if _data_type == "PathCircle":
            instance.actual_instance = PathCircle.from_json(json_str)
            return instance

        # check if data type is `PathCubicSpline`
        if _data_type == "PathCubicSpline":
            instance.actual_instance = PathCubicSpline.from_json(json_str)
            return instance

        # check if data type is `PathJointPTP`
        if _data_type == "PathJointPTP":
            instance.actual_instance = PathJointPTP.from_json(json_str)
            return instance

        # check if data type is `PathLine`
        if _data_type == "PathLine":
            instance.actual_instance = PathLine.from_json(json_str)
            return instance

        # deserialize data into PathCartesianPTP
        try:
            instance.actual_instance = PathCartesianPTP.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into PathCubicSpline
        try:
            instance.actual_instance = PathCubicSpline.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into PathLine
        try:
            instance.actual_instance = PathLine.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into PathCircle
        try:
            instance.actual_instance = PathCircle.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into PathJointPTP
        try:
            instance.actual_instance = PathJointPTP.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into MotionCommandPath with oneOf schemas: PathCartesianPTP, PathCircle, PathCubicSpline, PathJointPTP, PathLine. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into MotionCommandPath with oneOf schemas: PathCartesianPTP, PathCircle, PathCubicSpline, PathJointPTP, PathLine. Details: " + ", ".join(error_messages))
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        if hasattr(self.actual_instance, "to_json") and callable(self.actual_instance.to_json):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(self) -> Optional[Union[Dict[str, Any], PathCartesianPTP, PathCircle, PathCubicSpline, PathJointPTP, PathLine]]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(self.actual_instance.to_dict):
            return self.actual_instance.to_dict()
        else:
            # primitive type
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())


