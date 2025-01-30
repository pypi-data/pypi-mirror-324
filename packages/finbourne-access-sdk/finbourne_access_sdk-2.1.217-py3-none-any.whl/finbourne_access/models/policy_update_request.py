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


from typing import Any, Dict, List, Optional
from pydantic.v1 import BaseModel, Field, StrictStr, conlist, constr
from finbourne_access.models.for_spec import ForSpec
from finbourne_access.models.grant import Grant
from finbourne_access.models.how_spec import HowSpec
from finbourne_access.models.if_expression import IfExpression
from finbourne_access.models.selector_definition import SelectorDefinition
from finbourne_access.models.template_metadata import TemplateMetadata
from finbourne_access.models.when_spec import WhenSpec

class PolicyUpdateRequest(BaseModel):
    """
    Update policy request  # noqa: E501
    """
    description: Optional[constr(strict=True, max_length=1024, min_length=0)] = Field(None, description="Description of what the policy will be used for")
    applications: Optional[conlist(StrictStr)] = Field(None, description="Applications this policy is used with")
    grant: Grant = Field(...)
    selectors: conlist(SelectorDefinition) = Field(..., description="Selectors that identify what resources this policy qualifies for")
    var_for: Optional[conlist(ForSpec)] = Field(None, alias="for", description="\"For Specification\" for when the policy is to be applied")
    var_if: Optional[conlist(IfExpression)] = Field(None, alias="if", description="\"If Specification\" for when the policy is to be applied")
    when: WhenSpec = Field(...)
    how: Optional[HowSpec] = None
    template_metadata: Optional[TemplateMetadata] = Field(None, alias="templateMetadata")
    __properties = ["description", "applications", "grant", "selectors", "for", "if", "when", "how", "templateMetadata"]

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
    def from_json(cls, json_str: str) -> PolicyUpdateRequest:
        """Create an instance of PolicyUpdateRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in selectors (list)
        _items = []
        if self.selectors:
            for _item in self.selectors:
                if _item:
                    _items.append(_item.to_dict())
            _dict['selectors'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in var_for (list)
        _items = []
        if self.var_for:
            for _item in self.var_for:
                if _item:
                    _items.append(_item.to_dict())
            _dict['for'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in var_if (list)
        _items = []
        if self.var_if:
            for _item in self.var_if:
                if _item:
                    _items.append(_item.to_dict())
            _dict['if'] = _items
        # override the default output from pydantic by calling `to_dict()` of when
        if self.when:
            _dict['when'] = self.when.to_dict()
        # override the default output from pydantic by calling `to_dict()` of how
        if self.how:
            _dict['how'] = self.how.to_dict()
        # override the default output from pydantic by calling `to_dict()` of template_metadata
        if self.template_metadata:
            _dict['templateMetadata'] = self.template_metadata.to_dict()
        # set to None if description (nullable) is None
        # and __fields_set__ contains the field
        if self.description is None and "description" in self.__fields_set__:
            _dict['description'] = None

        # set to None if applications (nullable) is None
        # and __fields_set__ contains the field
        if self.applications is None and "applications" in self.__fields_set__:
            _dict['applications'] = None

        # set to None if var_for (nullable) is None
        # and __fields_set__ contains the field
        if self.var_for is None and "var_for" in self.__fields_set__:
            _dict['for'] = None

        # set to None if var_if (nullable) is None
        # and __fields_set__ contains the field
        if self.var_if is None and "var_if" in self.__fields_set__:
            _dict['if'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PolicyUpdateRequest:
        """Create an instance of PolicyUpdateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return PolicyUpdateRequest.parse_obj(obj)

        _obj = PolicyUpdateRequest.parse_obj({
            "description": obj.get("description"),
            "applications": obj.get("applications"),
            "grant": obj.get("grant"),
            "selectors": [SelectorDefinition.from_dict(_item) for _item in obj.get("selectors")] if obj.get("selectors") is not None else None,
            "var_for": [ForSpec.from_dict(_item) for _item in obj.get("for")] if obj.get("for") is not None else None,
            "var_if": [IfExpression.from_dict(_item) for _item in obj.get("if")] if obj.get("if") is not None else None,
            "when": WhenSpec.from_dict(obj.get("when")) if obj.get("when") is not None else None,
            "how": HowSpec.from_dict(obj.get("how")) if obj.get("how") is not None else None,
            "template_metadata": TemplateMetadata.from_dict(obj.get("templateMetadata")) if obj.get("templateMetadata") is not None else None
        })
        return _obj
