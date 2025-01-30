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

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class TestPointByTestSuiteModel(BaseModel):
    """
    TestPointByTestSuiteModel
    """ # noqa: E501
    id: StrictStr = Field(description="Test point unique internal identifier")
    tester_id: Optional[StrictStr] = Field(default=None, description="Tester who is responded for the test unique internal identifier", alias="testerId")
    work_item_id: Optional[StrictStr] = Field(default=None, description="Workitem to which test point relates unique identifier", alias="workItemId")
    configuration_id: Optional[StrictStr] = Field(default=None, description="Configuration to which test point relates unique identifier", alias="configurationId")
    status: Optional[StrictStr] = Field(default=None, description="Test point status   Applies one of these values: Blocked, NoResults, Failed, Passed")
    last_test_result_id: Optional[StrictStr] = Field(default=None, description="Last test result unique identifier", alias="lastTestResultId")
    iteration_id: StrictStr = Field(description="Iteration unique identifier", alias="iterationId")
    work_item_median_duration: Optional[StrictInt] = Field(default=None, description="Median duration of work item the test point represents", alias="workItemMedianDuration")
    __properties: ClassVar[List[str]] = ["id", "testerId", "workItemId", "configurationId", "status", "lastTestResultId", "iterationId", "workItemMedianDuration"]

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
        """Create an instance of TestPointByTestSuiteModel from a JSON string"""
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
        # set to None if tester_id (nullable) is None
        # and model_fields_set contains the field
        if self.tester_id is None and "tester_id" in self.model_fields_set:
            _dict['testerId'] = None

        # set to None if work_item_id (nullable) is None
        # and model_fields_set contains the field
        if self.work_item_id is None and "work_item_id" in self.model_fields_set:
            _dict['workItemId'] = None

        # set to None if configuration_id (nullable) is None
        # and model_fields_set contains the field
        if self.configuration_id is None and "configuration_id" in self.model_fields_set:
            _dict['configurationId'] = None

        # set to None if status (nullable) is None
        # and model_fields_set contains the field
        if self.status is None and "status" in self.model_fields_set:
            _dict['status'] = None

        # set to None if last_test_result_id (nullable) is None
        # and model_fields_set contains the field
        if self.last_test_result_id is None and "last_test_result_id" in self.model_fields_set:
            _dict['lastTestResultId'] = None

        # set to None if work_item_median_duration (nullable) is None
        # and model_fields_set contains the field
        if self.work_item_median_duration is None and "work_item_median_duration" in self.model_fields_set:
            _dict['workItemMedianDuration'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TestPointByTestSuiteModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "testerId": obj.get("testerId"),
            "workItemId": obj.get("workItemId"),
            "configurationId": obj.get("configurationId"),
            "status": obj.get("status"),
            "lastTestResultId": obj.get("lastTestResultId"),
            "iterationId": obj.get("iterationId"),
            "workItemMedianDuration": obj.get("workItemMedianDuration")
        })
        return _obj


