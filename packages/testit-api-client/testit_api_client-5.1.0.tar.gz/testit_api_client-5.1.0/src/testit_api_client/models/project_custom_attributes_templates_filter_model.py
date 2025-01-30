# coding: utf-8

"""
    API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: v2.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from testit_api_client.models.custom_attribute_types_enum import CustomAttributeTypesEnum
from typing import Optional, Set
from typing_extensions import Self

class ProjectCustomAttributesTemplatesFilterModel(BaseModel):
    """
    Collection of filters to apply to search
    """ # noqa: E501
    name: Optional[StrictStr] = Field(default=None, description="Name of custom attribute template")
    custom_attribute_types: Optional[List[CustomAttributeTypesEnum]] = Field(default=None, description="Collection of custom attributes types", alias="customAttributeTypes")
    __properties: ClassVar[List[str]] = ["name", "customAttributeTypes"]

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
        """Create an instance of ProjectCustomAttributesTemplatesFilterModel from a JSON string"""
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
        # set to None if name (nullable) is None
        # and model_fields_set contains the field
        if self.name is None and "name" in self.model_fields_set:
            _dict['name'] = None

        # set to None if custom_attribute_types (nullable) is None
        # and model_fields_set contains the field
        if self.custom_attribute_types is None and "custom_attribute_types" in self.model_fields_set:
            _dict['customAttributeTypes'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ProjectCustomAttributesTemplatesFilterModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "customAttributeTypes": obj.get("customAttributeTypes")
        })
        return _obj


