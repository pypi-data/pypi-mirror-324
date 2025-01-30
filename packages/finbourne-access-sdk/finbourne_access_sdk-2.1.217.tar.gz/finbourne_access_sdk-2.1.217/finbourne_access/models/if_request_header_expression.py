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


from typing import Any, Dict, Optional
from pydantic.v1 import BaseModel, Field, constr
from finbourne_access.models.text_operator import TextOperator

class IfRequestHeaderExpression(BaseModel):
    """
    IfRequestHeaderExpression
    """
    header_name: constr(strict=True, max_length=1024, min_length=1) = Field(..., alias="headerName")
    operator: TextOperator = Field(...)
    value: Optional[constr(strict=True, max_length=4096, min_length=0)] = None
    __properties = ["headerName", "operator", "value"]

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
    def from_json(cls, json_str: str) -> IfRequestHeaderExpression:
        """Create an instance of IfRequestHeaderExpression from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if value (nullable) is None
        # and __fields_set__ contains the field
        if self.value is None and "value" in self.__fields_set__:
            _dict['value'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> IfRequestHeaderExpression:
        """Create an instance of IfRequestHeaderExpression from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return IfRequestHeaderExpression.parse_obj(obj)

        _obj = IfRequestHeaderExpression.parse_obj({
            "header_name": obj.get("headerName"),
            "operator": obj.get("operator"),
            "value": obj.get("value")
        })
        return _obj
