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

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from testit_api_client.models.tag_post_model import TagPostModel
from testit_api_client.models.test_suite_test_plan_api_model import TestSuiteTestPlanApiModel
from typing import Optional, Set
from typing_extensions import Self

class CreateTestPlanApiModel(BaseModel):
    """
    CreateTestPlanApiModel
    """ # noqa: E501
    tags: Optional[List[TagPostModel]] = Field(default=None, description="Test plan tag names collection")
    name: Annotated[str, Field(min_length=0, strict=True, max_length=450)] = Field(description="Test plan name")
    start_date: Optional[datetime] = Field(default=None, description="Date and time of test plan start", alias="startDate")
    end_date: Optional[datetime] = Field(default=None, description="Date and time of test plan end", alias="endDate")
    description: Optional[Annotated[str, Field(min_length=0, strict=True, max_length=100000)]] = Field(default=None, description="Test plan description")
    build: Optional[Annotated[str, Field(min_length=0, strict=True, max_length=450)]] = Field(default=None, description="Build of the application on which test plan is executed")
    project_id: StrictStr = Field(description="Project unique identifier", alias="projectId")
    product_name: Optional[Annotated[str, Field(min_length=0, strict=True, max_length=450)]] = Field(default=None, description="Name of the testing product", alias="productName")
    has_automatic_duration_timer: Optional[StrictBool] = Field(default=None, description="Boolean flag defines if test plan has automatic duration timer", alias="hasAutomaticDurationTimer")
    attributes: Dict[str, Any] = Field(description="Key value pair of test plan custom attributes")
    test_suite: Optional[TestSuiteTestPlanApiModel] = Field(default=None, alias="testSuite")
    __properties: ClassVar[List[str]] = ["tags", "name", "startDate", "endDate", "description", "build", "projectId", "productName", "hasAutomaticDurationTimer", "attributes", "testSuite"]

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
        """Create an instance of CreateTestPlanApiModel from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in tags (list)
        _items = []
        if self.tags:
            for _item_tags in self.tags:
                if _item_tags:
                    _items.append(_item_tags.to_dict())
            _dict['tags'] = _items
        # override the default output from pydantic by calling `to_dict()` of test_suite
        if self.test_suite:
            _dict['testSuite'] = self.test_suite.to_dict()
        # set to None if tags (nullable) is None
        # and model_fields_set contains the field
        if self.tags is None and "tags" in self.model_fields_set:
            _dict['tags'] = None

        # set to None if start_date (nullable) is None
        # and model_fields_set contains the field
        if self.start_date is None and "start_date" in self.model_fields_set:
            _dict['startDate'] = None

        # set to None if end_date (nullable) is None
        # and model_fields_set contains the field
        if self.end_date is None and "end_date" in self.model_fields_set:
            _dict['endDate'] = None

        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict['description'] = None

        # set to None if build (nullable) is None
        # and model_fields_set contains the field
        if self.build is None and "build" in self.model_fields_set:
            _dict['build'] = None

        # set to None if product_name (nullable) is None
        # and model_fields_set contains the field
        if self.product_name is None and "product_name" in self.model_fields_set:
            _dict['productName'] = None

        # set to None if has_automatic_duration_timer (nullable) is None
        # and model_fields_set contains the field
        if self.has_automatic_duration_timer is None and "has_automatic_duration_timer" in self.model_fields_set:
            _dict['hasAutomaticDurationTimer'] = None

        # set to None if test_suite (nullable) is None
        # and model_fields_set contains the field
        if self.test_suite is None and "test_suite" in self.model_fields_set:
            _dict['testSuite'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CreateTestPlanApiModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "tags": [TagPostModel.from_dict(_item) for _item in obj["tags"]] if obj.get("tags") is not None else None,
            "name": obj.get("name"),
            "startDate": obj.get("startDate"),
            "endDate": obj.get("endDate"),
            "description": obj.get("description"),
            "build": obj.get("build"),
            "projectId": obj.get("projectId"),
            "productName": obj.get("productName"),
            "hasAutomaticDurationTimer": obj.get("hasAutomaticDurationTimer"),
            "attributes": obj.get("attributes"),
            "testSuite": TestSuiteTestPlanApiModel.from_dict(obj["testSuite"]) if obj.get("testSuite") is not None else None
        })
        return _obj


