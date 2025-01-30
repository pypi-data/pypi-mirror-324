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

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set
from typing_extensions import Self

class InitializeMovementRequest(BaseModel):
    """
    Sets up connection by locking a trajectory for execution. The robot controller mode is set to control mode. ATTENTION: This request has to be sent before any StartMovementRequest is sent.            If initializing the movement was successful, no further movements can be initialized. To execute another trajectory, another connection has to be established. 
    """ # noqa: E501
    message_type: Optional[StrictStr] = Field(default=None, description="Type specifier for server, set automatically. ")
    trajectory: StrictStr = Field(description="The trajectory which should be executed and locked to the connection. Get information about the trajectory via [getMotionTrajectory](getMotionTrajectory). ")
    initial_location: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Location on trajectory where the execution will start. The default value is the start (forward movement) or end (backward movement) of the trajectory. If you want to start your movement from an arbitrary location, e.g. in combination with [streamMoveToTrajectoryViaJointPTP](streamMoveToTrajectoryViaJointPTP), set the location by respecting the following format: - The location is a scalar value that defines a position along a path, typically ranging from 0 to `n`,   where `n` denotes the number of motion commands - Each integer value of the location corresponds to a specific motion command,   while non-integer values interpolate positions within the segments. - The location is calculated from the joint path ")
    response_rate: Optional[StrictInt] = Field(default=None, description="Update rate for the response message in milliseconds (ms). Default is 200 ms. Recommendation: As Wandelbots NOVA updates states in the controller's step rate, use either the controller's step rate or a multiple of it.                 Wandelbots NOVA will not interpolate the state but rather round it to the nearest step rate below the configured response rate. Minimal response rate is the step rate of controller. ")
    response_coordinate_system: Optional[StrictStr] = Field(default=None, description="Unique identifier addressing a coordinate system to which the responses are transformed. If not set, world coordinate system is used. ")
    __properties: ClassVar[List[str]] = ["message_type", "trajectory", "initial_location", "response_rate", "response_coordinate_system"]

    @field_validator('message_type')
    def message_type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['InitializeMovementRequest']):
            raise ValueError("must be one of enum values ('InitializeMovementRequest')")
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
        """Create an instance of InitializeMovementRequest from a JSON string"""
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
        """Create an instance of InitializeMovementRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "message_type": obj.get("message_type"),
            "trajectory": obj.get("trajectory"),
            "initial_location": obj.get("initial_location"),
            "response_rate": obj.get("response_rate"),
            "response_coordinate_system": obj.get("response_coordinate_system")
        })
        return _obj


