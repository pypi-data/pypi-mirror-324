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
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from testit_api_client.models.autotest_result_outcome import AutotestResultOutcome
from testit_api_client.models.rerun_test_result_model import RerunTestResultModel
from typing import Optional, Set
from typing_extensions import Self

class AutotestResultHistoricalGetModel(BaseModel):
    """
    AutotestResultHistoricalGetModel
    """ # noqa: E501
    modified_date: Optional[datetime] = Field(default=None, alias="modifiedDate")
    modified_by_id: Optional[StrictStr] = Field(default=None, alias="modifiedById")
    test_plan_id: Optional[StrictStr] = Field(default=None, alias="testPlanId")
    test_plan_global_id: Optional[StrictInt] = Field(default=None, alias="testPlanGlobalId")
    test_plan_name: Optional[StrictStr] = Field(default=None, alias="testPlanName")
    duration: Optional[StrictInt] = None
    id: StrictStr
    created_date: datetime = Field(alias="createdDate")
    created_by_id: StrictStr = Field(alias="createdById")
    created_by_name: StrictStr = Field(alias="createdByName")
    test_run_id: StrictStr = Field(alias="testRunId")
    test_run_name: Optional[StrictStr] = Field(default=None, alias="testRunName")
    configuration_id: StrictStr = Field(alias="configurationId")
    configuration_name: StrictStr = Field(alias="configurationName")
    outcome: AutotestResultOutcome
    launch_source: Optional[StrictStr] = Field(default=None, alias="launchSource")
    rerun_count: StrictInt = Field(alias="rerunCount")
    rerun_test_results: List[RerunTestResultModel] = Field(alias="rerunTestResults")
    __properties: ClassVar[List[str]] = ["modifiedDate", "modifiedById", "testPlanId", "testPlanGlobalId", "testPlanName", "duration", "id", "createdDate", "createdById", "createdByName", "testRunId", "testRunName", "configurationId", "configurationName", "outcome", "launchSource", "rerunCount", "rerunTestResults"]

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
        """Create an instance of AutotestResultHistoricalGetModel from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in rerun_test_results (list)
        _items = []
        if self.rerun_test_results:
            for _item_rerun_test_results in self.rerun_test_results:
                if _item_rerun_test_results:
                    _items.append(_item_rerun_test_results.to_dict())
            _dict['rerunTestResults'] = _items
        # set to None if modified_date (nullable) is None
        # and model_fields_set contains the field
        if self.modified_date is None and "modified_date" in self.model_fields_set:
            _dict['modifiedDate'] = None

        # set to None if modified_by_id (nullable) is None
        # and model_fields_set contains the field
        if self.modified_by_id is None and "modified_by_id" in self.model_fields_set:
            _dict['modifiedById'] = None

        # set to None if test_plan_id (nullable) is None
        # and model_fields_set contains the field
        if self.test_plan_id is None and "test_plan_id" in self.model_fields_set:
            _dict['testPlanId'] = None

        # set to None if test_plan_global_id (nullable) is None
        # and model_fields_set contains the field
        if self.test_plan_global_id is None and "test_plan_global_id" in self.model_fields_set:
            _dict['testPlanGlobalId'] = None

        # set to None if test_plan_name (nullable) is None
        # and model_fields_set contains the field
        if self.test_plan_name is None and "test_plan_name" in self.model_fields_set:
            _dict['testPlanName'] = None

        # set to None if duration (nullable) is None
        # and model_fields_set contains the field
        if self.duration is None and "duration" in self.model_fields_set:
            _dict['duration'] = None

        # set to None if test_run_name (nullable) is None
        # and model_fields_set contains the field
        if self.test_run_name is None and "test_run_name" in self.model_fields_set:
            _dict['testRunName'] = None

        # set to None if launch_source (nullable) is None
        # and model_fields_set contains the field
        if self.launch_source is None and "launch_source" in self.model_fields_set:
            _dict['launchSource'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AutotestResultHistoricalGetModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "modifiedDate": obj.get("modifiedDate"),
            "modifiedById": obj.get("modifiedById"),
            "testPlanId": obj.get("testPlanId"),
            "testPlanGlobalId": obj.get("testPlanGlobalId"),
            "testPlanName": obj.get("testPlanName"),
            "duration": obj.get("duration"),
            "id": obj.get("id"),
            "createdDate": obj.get("createdDate"),
            "createdById": obj.get("createdById"),
            "createdByName": obj.get("createdByName"),
            "testRunId": obj.get("testRunId"),
            "testRunName": obj.get("testRunName"),
            "configurationId": obj.get("configurationId"),
            "configurationName": obj.get("configurationName"),
            "outcome": obj.get("outcome"),
            "launchSource": obj.get("launchSource"),
            "rerunCount": obj.get("rerunCount"),
            "rerunTestResults": [RerunTestResultModel.from_dict(_item) for _item in obj["rerunTestResults"]] if obj.get("rerunTestResults") is not None else None
        })
        return _obj


