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

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from testit_api_client.models.guid_extraction_model import GuidExtractionModel
from typing import Optional, Set
from typing_extensions import Self

class ConfigurationExtractionModel(BaseModel):
    """
    ConfigurationExtractionModel
    """ # noqa: E501
    ids: Optional[GuidExtractionModel] = Field(default=None, description="Extraction parameters for configurations")
    project_ids: Optional[GuidExtractionModel] = Field(default=None, description="Extraction parameters for projects", alias="projectIds")
    __properties: ClassVar[List[str]] = ["ids", "projectIds"]

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
        """Create an instance of ConfigurationExtractionModel from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of ids
        if self.ids:
            _dict['ids'] = self.ids.to_dict()
        # override the default output from pydantic by calling `to_dict()` of project_ids
        if self.project_ids:
            _dict['projectIds'] = self.project_ids.to_dict()
        # set to None if ids (nullable) is None
        # and model_fields_set contains the field
        if self.ids is None and "ids" in self.model_fields_set:
            _dict['ids'] = None

        # set to None if project_ids (nullable) is None
        # and model_fields_set contains the field
        if self.project_ids is None and "project_ids" in self.model_fields_set:
            _dict['projectIds'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ConfigurationExtractionModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "ids": GuidExtractionModel.from_dict(obj["ids"]) if obj.get("ids") is not None else None,
            "projectIds": GuidExtractionModel.from_dict(obj["projectIds"]) if obj.get("projectIds") is not None else None
        })
        return _obj


