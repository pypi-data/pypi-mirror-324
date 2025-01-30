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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from testit_api_client.models.test_status_api_result import TestStatusApiResult
from typing import Optional, Set
from typing_extensions import Self

class TestPoint(BaseModel):
    """
    TestPoint
    """ # noqa: E501
    id: StrictStr = Field(description="Unique ID of the entity")
    is_deleted: StrictBool = Field(description="Indicates if the entity is deleted", alias="isDeleted")
    tester_id: Optional[StrictStr] = Field(default=None, alias="testerId")
    iteration_id: StrictStr = Field(alias="iterationId")
    work_item_id: Optional[StrictStr] = Field(default=None, alias="workItemId")
    configuration_id: Optional[StrictStr] = Field(default=None, alias="configurationId")
    test_suite_id: StrictStr = Field(alias="testSuiteId")
    status: Optional[StrictStr] = None
    status_model: Optional[TestStatusApiResult] = Field(default=None, alias="statusModel")
    last_test_result_id: Optional[StrictStr] = Field(default=None, alias="lastTestResultId")
    __properties: ClassVar[List[str]] = ["id", "isDeleted", "testerId", "iterationId", "workItemId", "configurationId", "testSuiteId", "status", "statusModel", "lastTestResultId"]

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
        """Create an instance of TestPoint from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of status_model
        if self.status_model:
            _dict['statusModel'] = self.status_model.to_dict()
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

        # set to None if status_model (nullable) is None
        # and model_fields_set contains the field
        if self.status_model is None and "status_model" in self.model_fields_set:
            _dict['statusModel'] = None

        # set to None if last_test_result_id (nullable) is None
        # and model_fields_set contains the field
        if self.last_test_result_id is None and "last_test_result_id" in self.model_fields_set:
            _dict['lastTestResultId'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TestPoint from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "isDeleted": obj.get("isDeleted"),
            "testerId": obj.get("testerId"),
            "iterationId": obj.get("iterationId"),
            "workItemId": obj.get("workItemId"),
            "configurationId": obj.get("configurationId"),
            "testSuiteId": obj.get("testSuiteId"),
            "status": obj.get("status"),
            "statusModel": TestStatusApiResult.from_dict(obj["statusModel"]) if obj.get("statusModel") is not None else None,
            "lastTestResultId": obj.get("lastTestResultId")
        })
        return _obj


