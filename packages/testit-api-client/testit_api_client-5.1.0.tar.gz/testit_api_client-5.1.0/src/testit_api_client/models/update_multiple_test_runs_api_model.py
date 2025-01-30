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
from testit_api_client.models.test_run_select_api_model import TestRunSelectApiModel
from testit_api_client.models.update_multiple_attachments_api_model import UpdateMultipleAttachmentsApiModel
from testit_api_client.models.update_multiple_links_api_model import UpdateMultipleLinksApiModel
from typing import Optional, Set
from typing_extensions import Self

class UpdateMultipleTestRunsApiModel(BaseModel):
    """
    UpdateMultipleTestRunsApiModel
    """ # noqa: E501
    select_model: TestRunSelectApiModel = Field(description="Test run selection model", alias="selectModel")
    description: Optional[StrictStr] = Field(default=None, description="Test run description")
    attachment_update_scheme: Optional[UpdateMultipleAttachmentsApiModel] = Field(default=None, description="Set of attachment ids", alias="attachmentUpdateScheme")
    link_update_scheme: Optional[UpdateMultipleLinksApiModel] = Field(default=None, description="Set of links", alias="linkUpdateScheme")
    __properties: ClassVar[List[str]] = ["selectModel", "description", "attachmentUpdateScheme", "linkUpdateScheme"]

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
        """Create an instance of UpdateMultipleTestRunsApiModel from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of select_model
        if self.select_model:
            _dict['selectModel'] = self.select_model.to_dict()
        # override the default output from pydantic by calling `to_dict()` of attachment_update_scheme
        if self.attachment_update_scheme:
            _dict['attachmentUpdateScheme'] = self.attachment_update_scheme.to_dict()
        # override the default output from pydantic by calling `to_dict()` of link_update_scheme
        if self.link_update_scheme:
            _dict['linkUpdateScheme'] = self.link_update_scheme.to_dict()
        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict['description'] = None

        # set to None if attachment_update_scheme (nullable) is None
        # and model_fields_set contains the field
        if self.attachment_update_scheme is None and "attachment_update_scheme" in self.model_fields_set:
            _dict['attachmentUpdateScheme'] = None

        # set to None if link_update_scheme (nullable) is None
        # and model_fields_set contains the field
        if self.link_update_scheme is None and "link_update_scheme" in self.model_fields_set:
            _dict['linkUpdateScheme'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UpdateMultipleTestRunsApiModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "selectModel": TestRunSelectApiModel.from_dict(obj["selectModel"]) if obj.get("selectModel") is not None else None,
            "description": obj.get("description"),
            "attachmentUpdateScheme": UpdateMultipleAttachmentsApiModel.from_dict(obj["attachmentUpdateScheme"]) if obj.get("attachmentUpdateScheme") is not None else None,
            "linkUpdateScheme": UpdateMultipleLinksApiModel.from_dict(obj["linkUpdateScheme"]) if obj.get("linkUpdateScheme") is not None else None
        })
        return _obj


