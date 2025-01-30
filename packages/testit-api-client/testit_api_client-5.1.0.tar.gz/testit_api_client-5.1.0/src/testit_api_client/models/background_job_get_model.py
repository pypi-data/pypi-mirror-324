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
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from testit_api_client.models.background_job_attachment_model import BackgroundJobAttachmentModel
from testit_api_client.models.background_job_state import BackgroundJobState
from testit_api_client.models.background_job_type import BackgroundJobType
from typing import Optional, Set
from typing_extensions import Self

class BackgroundJobGetModel(BaseModel):
    """
    BackgroundJobGetModel
    """ # noqa: E501
    id: StrictStr
    job_id: StrictStr = Field(alias="jobId")
    job_type: BackgroundJobType = Field(alias="jobType")
    state: BackgroundJobState
    is_deleted: StrictBool = Field(alias="isDeleted")
    progress: StrictInt
    created_date: datetime = Field(alias="createdDate")
    start_date: Optional[datetime] = Field(default=None, alias="startDate")
    end_date: Optional[datetime] = Field(default=None, alias="endDate")
    error: Optional[StrictStr] = None
    attachments: List[BackgroundJobAttachmentModel]
    __properties: ClassVar[List[str]] = ["id", "jobId", "jobType", "state", "isDeleted", "progress", "createdDate", "startDate", "endDate", "error", "attachments"]

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
        """Create an instance of BackgroundJobGetModel from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in attachments (list)
        _items = []
        if self.attachments:
            for _item_attachments in self.attachments:
                if _item_attachments:
                    _items.append(_item_attachments.to_dict())
            _dict['attachments'] = _items
        # set to None if start_date (nullable) is None
        # and model_fields_set contains the field
        if self.start_date is None and "start_date" in self.model_fields_set:
            _dict['startDate'] = None

        # set to None if end_date (nullable) is None
        # and model_fields_set contains the field
        if self.end_date is None and "end_date" in self.model_fields_set:
            _dict['endDate'] = None

        # set to None if error (nullable) is None
        # and model_fields_set contains the field
        if self.error is None and "error" in self.model_fields_set:
            _dict['error'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of BackgroundJobGetModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "jobId": obj.get("jobId"),
            "jobType": obj.get("jobType"),
            "state": obj.get("state"),
            "isDeleted": obj.get("isDeleted"),
            "progress": obj.get("progress"),
            "createdDate": obj.get("createdDate"),
            "startDate": obj.get("startDate"),
            "endDate": obj.get("endDate"),
            "error": obj.get("error"),
            "attachments": [BackgroundJobAttachmentModel.from_dict(_item) for _item in obj["attachments"]] if obj.get("attachments") is not None else None
        })
        return _obj


