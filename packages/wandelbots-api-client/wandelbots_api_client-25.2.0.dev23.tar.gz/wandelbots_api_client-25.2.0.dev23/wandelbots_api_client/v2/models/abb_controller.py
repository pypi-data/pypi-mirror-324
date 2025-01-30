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

from pydantic import BaseModel, ConfigDict, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from wandelbots_api_client.v2.models.abb_controller_egm_server import AbbControllerEgmServer
from typing import Optional, Set
from typing_extensions import Self

class AbbController(BaseModel):
    """
    The configuration of a physical ABB robot controller has to contain IP address. Additionally an EGM server configuration has to be specified in order to control the robot. Deploying the server is a functionality of this API. 
    """ # noqa: E501
    kind: Optional[StrictStr] = 'AbbController'
    controller_ip: StrictStr
    egm_server: AbbControllerEgmServer
    __properties: ClassVar[List[str]] = ["kind", "controller_ip", "egm_server"]

    @field_validator('kind')
    def kind_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['AbbController']):
            raise ValueError("must be one of enum values ('AbbController')")
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
        """Create an instance of AbbController from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of egm_server
        if self.egm_server:
            _dict['egm_server'] = self.egm_server.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AbbController from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "kind": obj.get("kind") if obj.get("kind") is not None else 'AbbController',
            "controller_ip": obj.get("controller_ip"),
            "egm_server": AbbControllerEgmServer.from_dict(obj["egm_server"]) if obj.get("egm_server") is not None else None
        })
        return _obj


