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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from testit_api_client.models.date_time_range_selector_model import DateTimeRangeSelectorModel
from testit_api_client.models.int32_range_selector_model import Int32RangeSelectorModel
from testit_api_client.models.project_type_model import ProjectTypeModel
from typing import Optional, Set
from typing_extensions import Self

class ProjectsFilterModel(BaseModel):
    """
    ProjectsFilterModel
    """ # noqa: E501
    name: Optional[Annotated[str, Field(min_length=0, strict=True, max_length=255)]] = Field(default=None, description="Specifies a project name to search for")
    is_favorite: Optional[StrictBool] = Field(default=None, description="Specifies a project favorite status to search for", alias="isFavorite")
    is_deleted: Optional[StrictBool] = Field(default=None, description="Specifies a project deleted status to search for", alias="isDeleted")
    test_cases_count: Optional[Int32RangeSelectorModel] = Field(default=None, description="Specifies a project range of test cases count to search for", alias="testCasesCount")
    checklists_count: Optional[Int32RangeSelectorModel] = Field(default=None, description="Specifies a project range of checklists count to search for", alias="checklistsCount")
    shared_steps_count: Optional[Int32RangeSelectorModel] = Field(default=None, description="Specifies a project range of shared steps count to search for", alias="sharedStepsCount")
    autotests_count: Optional[Int32RangeSelectorModel] = Field(default=None, description="Specifies a project range of autotests count to search for", alias="autotestsCount")
    global_ids: Optional[List[StrictInt]] = Field(default=None, description="Specifies a project global IDs to search for", alias="globalIds")
    created_date: Optional[DateTimeRangeSelectorModel] = Field(default=None, description="Specifies a project range of creation date to search for", alias="createdDate")
    created_by_ids: Optional[List[StrictStr]] = Field(default=None, description="Specifies an autotest creator IDs to search for", alias="createdByIds")
    types: Optional[List[ProjectTypeModel]] = Field(default=None, description="Collection of project types to search for")
    __properties: ClassVar[List[str]] = ["name", "isFavorite", "isDeleted", "testCasesCount", "checklistsCount", "sharedStepsCount", "autotestsCount", "globalIds", "createdDate", "createdByIds", "types"]

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
        """Create an instance of ProjectsFilterModel from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of test_cases_count
        if self.test_cases_count:
            _dict['testCasesCount'] = self.test_cases_count.to_dict()
        # override the default output from pydantic by calling `to_dict()` of checklists_count
        if self.checklists_count:
            _dict['checklistsCount'] = self.checklists_count.to_dict()
        # override the default output from pydantic by calling `to_dict()` of shared_steps_count
        if self.shared_steps_count:
            _dict['sharedStepsCount'] = self.shared_steps_count.to_dict()
        # override the default output from pydantic by calling `to_dict()` of autotests_count
        if self.autotests_count:
            _dict['autotestsCount'] = self.autotests_count.to_dict()
        # override the default output from pydantic by calling `to_dict()` of created_date
        if self.created_date:
            _dict['createdDate'] = self.created_date.to_dict()
        # set to None if name (nullable) is None
        # and model_fields_set contains the field
        if self.name is None and "name" in self.model_fields_set:
            _dict['name'] = None

        # set to None if is_favorite (nullable) is None
        # and model_fields_set contains the field
        if self.is_favorite is None and "is_favorite" in self.model_fields_set:
            _dict['isFavorite'] = None

        # set to None if is_deleted (nullable) is None
        # and model_fields_set contains the field
        if self.is_deleted is None and "is_deleted" in self.model_fields_set:
            _dict['isDeleted'] = None

        # set to None if test_cases_count (nullable) is None
        # and model_fields_set contains the field
        if self.test_cases_count is None and "test_cases_count" in self.model_fields_set:
            _dict['testCasesCount'] = None

        # set to None if checklists_count (nullable) is None
        # and model_fields_set contains the field
        if self.checklists_count is None and "checklists_count" in self.model_fields_set:
            _dict['checklistsCount'] = None

        # set to None if shared_steps_count (nullable) is None
        # and model_fields_set contains the field
        if self.shared_steps_count is None and "shared_steps_count" in self.model_fields_set:
            _dict['sharedStepsCount'] = None

        # set to None if autotests_count (nullable) is None
        # and model_fields_set contains the field
        if self.autotests_count is None and "autotests_count" in self.model_fields_set:
            _dict['autotestsCount'] = None

        # set to None if global_ids (nullable) is None
        # and model_fields_set contains the field
        if self.global_ids is None and "global_ids" in self.model_fields_set:
            _dict['globalIds'] = None

        # set to None if created_date (nullable) is None
        # and model_fields_set contains the field
        if self.created_date is None and "created_date" in self.model_fields_set:
            _dict['createdDate'] = None

        # set to None if created_by_ids (nullable) is None
        # and model_fields_set contains the field
        if self.created_by_ids is None and "created_by_ids" in self.model_fields_set:
            _dict['createdByIds'] = None

        # set to None if types (nullable) is None
        # and model_fields_set contains the field
        if self.types is None and "types" in self.model_fields_set:
            _dict['types'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ProjectsFilterModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "isFavorite": obj.get("isFavorite"),
            "isDeleted": obj.get("isDeleted"),
            "testCasesCount": Int32RangeSelectorModel.from_dict(obj["testCasesCount"]) if obj.get("testCasesCount") is not None else None,
            "checklistsCount": Int32RangeSelectorModel.from_dict(obj["checklistsCount"]) if obj.get("checklistsCount") is not None else None,
            "sharedStepsCount": Int32RangeSelectorModel.from_dict(obj["sharedStepsCount"]) if obj.get("sharedStepsCount") is not None else None,
            "autotestsCount": Int32RangeSelectorModel.from_dict(obj["autotestsCount"]) if obj.get("autotestsCount") is not None else None,
            "globalIds": obj.get("globalIds"),
            "createdDate": DateTimeRangeSelectorModel.from_dict(obj["createdDate"]) if obj.get("createdDate") is not None else None,
            "createdByIds": obj.get("createdByIds"),
            "types": obj.get("types")
        })
        return _obj


