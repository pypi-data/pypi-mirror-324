# coding: utf-8

"""
    FINBOURNE Access Management API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, Dict
from pydantic.v1 import BaseModel, Field, constr, validator
from finbourne_access.models.policy_id_role_resource import PolicyIdRoleResource

class UserRoleCreationRequest(BaseModel):
    """
    Dto used to request creating a user's role  # noqa: E501
    """
    user_id: constr(strict=True, min_length=1) = Field(..., alias="userId", description="The Id of the user for whom to create the role.")
    resource: PolicyIdRoleResource = Field(...)
    __properties = ["userId", "resource"]

    @validator('user_id')
    def user_id_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^(?=.*[a-zA-Z])[\w][\w +-]{2,100}$", value):
            raise ValueError(r"must validate the regular expression /^(?=.*[a-zA-Z])[\w][\w +-]{2,100}$/")
        return value

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def __str__(self):
        """For `print` and `pprint`"""
        return pprint.pformat(self.dict(by_alias=False))

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> UserRoleCreationRequest:
        """Create an instance of UserRoleCreationRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of resource
        if self.resource:
            _dict['resource'] = self.resource.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UserRoleCreationRequest:
        """Create an instance of UserRoleCreationRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UserRoleCreationRequest.parse_obj(obj)

        _obj = UserRoleCreationRequest.parse_obj({
            "user_id": obj.get("userId"),
            "resource": PolicyIdRoleResource.from_dict(obj.get("resource")) if obj.get("resource") is not None else None
        })
        return _obj
