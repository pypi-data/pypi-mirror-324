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

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from wandelbots_api_client.models.circle import Circle
from wandelbots_api_client.models.command_settings import CommandSettings
from wandelbots_api_client.models.cubic_spline import CubicSpline
from wandelbots_api_client.models.joints import Joints
from wandelbots_api_client.models.pose import Pose
from typing import Optional, Set
from typing_extensions import Self

class Command(BaseModel):
    """
    A command is a single motion command (line, circle, joint_ptp, cartesian_ptp, cubic_spline) with corresponding settings (limits, blending). The motion commands are a flattened union/oneof type. Only set one of the motion commands per command. A motion command always starts at the end of the previous motion command. Subsequently, a plan request must have start joint configuration to plan a well defined motion.
    """ # noqa: E501
    settings: Optional[CommandSettings] = Field(default=None, description="Command settings for a single motion command. Allow blending between two motion commands or override limits on a motion command level.")
    line: Optional[Pose] = Field(default=None, description="A line is representing a straight line from start position to provided target position. The orientation is calculated via a quaternion [slerp](https://en.wikipedia.org/wiki/Slerp) from start orienation to provided target orientation.")
    circle: Optional[Circle] = Field(default=None, description="A circular constructs a circle in translative space from start position, provided via position, and provided target position. The orientation is calculated via a [bezier spline](https://en.wikipedia.org/wiki/B%C3%A9zier_curve) from start orienation to provided target orientation. The via point defines the control point for the bezier spline. Therefore, the control point will not be hit directly.")
    joint_ptp: Optional[Joints] = Field(default=None, description="A joint point-to-point is representing a line in joint space. All joints will be moved synchronously.")
    cartesian_ptp: Optional[Pose] = Field(default=None, description="A cartesian point-to-point is representing a joint point-to-point motion from start point to provided target pose. This is a joint point-to-point as well, but the target is given in cartesian space. The target joint configuration will be calculated to be in the same kinematic configuration as the start point is. If that is not possible, planning will fail.")
    cubic_spline: Optional[CubicSpline] = Field(default=None, description="A [cubic spline](https://de.wikipedia.org/wiki/Spline-Interpolation) is representing a cartesian cubic spline in translative and orientational space from start point to provided target pose via control points.")
    __properties: ClassVar[List[str]] = ["settings", "line", "circle", "joint_ptp", "cartesian_ptp", "cubic_spline"]

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
        """Create an instance of Command from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of settings
        if self.settings:
            _dict['settings'] = self.settings.to_dict()
        # override the default output from pydantic by calling `to_dict()` of line
        if self.line:
            _dict['line'] = self.line.to_dict()
        # override the default output from pydantic by calling `to_dict()` of circle
        if self.circle:
            _dict['circle'] = self.circle.to_dict()
        # override the default output from pydantic by calling `to_dict()` of joint_ptp
        if self.joint_ptp:
            _dict['joint_ptp'] = self.joint_ptp.to_dict()
        # override the default output from pydantic by calling `to_dict()` of cartesian_ptp
        if self.cartesian_ptp:
            _dict['cartesian_ptp'] = self.cartesian_ptp.to_dict()
        # override the default output from pydantic by calling `to_dict()` of cubic_spline
        if self.cubic_spline:
            _dict['cubic_spline'] = self.cubic_spline.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Command from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "settings": CommandSettings.from_dict(obj["settings"]) if obj.get("settings") is not None else None,
            "line": Pose.from_dict(obj["line"]) if obj.get("line") is not None else None,
            "circle": Circle.from_dict(obj["circle"]) if obj.get("circle") is not None else None,
            "joint_ptp": Joints.from_dict(obj["joint_ptp"]) if obj.get("joint_ptp") is not None else None,
            "cartesian_ptp": Pose.from_dict(obj["cartesian_ptp"]) if obj.get("cartesian_ptp") is not None else None,
            "cubic_spline": CubicSpline.from_dict(obj["cubic_spline"]) if obj.get("cubic_spline") is not None else None
        })
        return _obj


