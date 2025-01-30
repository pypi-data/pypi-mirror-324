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
from testit_api_client.models.work_item_step_change_view_model import WorkItemStepChangeViewModel
from typing import Optional, Set
from typing_extensions import Self

class WorkItemStepChangeViewModelArrayChangedFieldWithDiffsViewModel(BaseModel):
    """
    WorkItemStepChangeViewModelArrayChangedFieldWithDiffsViewModel
    """ # noqa: E501
    diff_value: Optional[List[WorkItemStepChangeViewModel]] = Field(default=None, alias="diffValue")
    old_value: Optional[List[WorkItemStepChangeViewModel]] = Field(default=None, alias="oldValue")
    new_value: Optional[List[WorkItemStepChangeViewModel]] = Field(default=None, alias="newValue")
    __properties: ClassVar[List[str]] = ["diffValue", "oldValue", "newValue"]

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
        """Create an instance of WorkItemStepChangeViewModelArrayChangedFieldWithDiffsViewModel from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in diff_value (list)
        _items = []
        if self.diff_value:
            for _item_diff_value in self.diff_value:
                if _item_diff_value:
                    _items.append(_item_diff_value.to_dict())
            _dict['diffValue'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in old_value (list)
        _items = []
        if self.old_value:
            for _item_old_value in self.old_value:
                if _item_old_value:
                    _items.append(_item_old_value.to_dict())
            _dict['oldValue'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in new_value (list)
        _items = []
        if self.new_value:
            for _item_new_value in self.new_value:
                if _item_new_value:
                    _items.append(_item_new_value.to_dict())
            _dict['newValue'] = _items
        # set to None if diff_value (nullable) is None
        # and model_fields_set contains the field
        if self.diff_value is None and "diff_value" in self.model_fields_set:
            _dict['diffValue'] = None

        # set to None if old_value (nullable) is None
        # and model_fields_set contains the field
        if self.old_value is None and "old_value" in self.model_fields_set:
            _dict['oldValue'] = None

        # set to None if new_value (nullable) is None
        # and model_fields_set contains the field
        if self.new_value is None and "new_value" in self.model_fields_set:
            _dict['newValue'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of WorkItemStepChangeViewModelArrayChangedFieldWithDiffsViewModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "diffValue": [WorkItemStepChangeViewModel.from_dict(_item) for _item in obj["diffValue"]] if obj.get("diffValue") is not None else None,
            "oldValue": [WorkItemStepChangeViewModel.from_dict(_item) for _item in obj["oldValue"]] if obj.get("oldValue") is not None else None,
            "newValue": [WorkItemStepChangeViewModel.from_dict(_item) for _item in obj["newValue"]] if obj.get("newValue") is not None else None
        })
        return _obj


