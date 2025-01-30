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
from typing import Optional, Set
from typing_extensions import Self

class StepPostModel(BaseModel):
    """
    StepPostModel
    """ # noqa: E501
    action: Optional[StrictStr] = None
    expected: Optional[StrictStr] = None
    test_data: Optional[StrictStr] = Field(default=None, alias="testData")
    comments: Optional[StrictStr] = None
    work_item_id: Optional[StrictStr] = Field(default=None, alias="workItemId")
    __properties: ClassVar[List[str]] = ["action", "expected", "testData", "comments", "workItemId"]

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
        """Create an instance of StepPostModel from a JSON string"""
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
        # set to None if action (nullable) is None
        # and model_fields_set contains the field
        if self.action is None and "action" in self.model_fields_set:
            _dict['action'] = None

        # set to None if expected (nullable) is None
        # and model_fields_set contains the field
        if self.expected is None and "expected" in self.model_fields_set:
            _dict['expected'] = None

        # set to None if test_data (nullable) is None
        # and model_fields_set contains the field
        if self.test_data is None and "test_data" in self.model_fields_set:
            _dict['testData'] = None

        # set to None if comments (nullable) is None
        # and model_fields_set contains the field
        if self.comments is None and "comments" in self.model_fields_set:
            _dict['comments'] = None

        # set to None if work_item_id (nullable) is None
        # and model_fields_set contains the field
        if self.work_item_id is None and "work_item_id" in self.model_fields_set:
            _dict['workItemId'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of StepPostModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "action": obj.get("action"),
            "expected": obj.get("expected"),
            "testData": obj.get("testData"),
            "comments": obj.get("comments"),
            "workItemId": obj.get("workItemId")
        })
        return _obj


