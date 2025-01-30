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
from typing_extensions import Annotated
from testit_api_client.models.request_type_request import RequestTypeRequest
from testit_api_client.models.web_hook_event_type_request import WebHookEventTypeRequest
from typing import Optional, Set
from typing_extensions import Self

class WebhooksFilterRequest(BaseModel):
    """
    WebhooksFilterRequest
    """ # noqa: E501
    name: Optional[Annotated[str, Field(min_length=0, strict=True, max_length=255)]] = Field(default=None, description="Specifies a webhook name to search for")
    event_types: Optional[List[WebHookEventTypeRequest]] = Field(default=None, description="Specifies a webhook event types to search for", alias="eventTypes")
    methods: Optional[List[RequestTypeRequest]] = Field(default=None, description="Specifies a webhook methods to search for")
    project_ids: Optional[List[StrictStr]] = Field(default=None, description="Specifies a webhook project IDs to search for", alias="projectIds")
    __properties: ClassVar[List[str]] = ["name", "eventTypes", "methods", "projectIds"]

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
        """Create an instance of WebhooksFilterRequest from a JSON string"""
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

        # set to None if event_types (nullable) is None
        # and model_fields_set contains the field
        if self.event_types is None and "event_types" in self.model_fields_set:
            _dict['eventTypes'] = None

        # set to None if methods (nullable) is None
        # and model_fields_set contains the field
        if self.methods is None and "methods" in self.model_fields_set:
            _dict['methods'] = None

        # set to None if project_ids (nullable) is None
        # and model_fields_set contains the field
        if self.project_ids is None and "project_ids" in self.model_fields_set:
            _dict['projectIds'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of WebhooksFilterRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "eventTypes": obj.get("eventTypes"),
            "methods": obj.get("methods"),
            "projectIds": obj.get("projectIds")
        })
        return _obj


