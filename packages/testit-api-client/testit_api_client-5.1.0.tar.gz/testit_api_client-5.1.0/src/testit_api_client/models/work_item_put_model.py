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
from testit_api_client.models.attachment_put_model import AttachmentPutModel
from testit_api_client.models.auto_test_id_model import AutoTestIdModel
from testit_api_client.models.iteration_put_model import IterationPutModel
from testit_api_client.models.link_put_model import LinkPutModel
from testit_api_client.models.step_put_model import StepPutModel
from testit_api_client.models.tag_put_model import TagPutModel
from testit_api_client.models.work_item_priority_model import WorkItemPriorityModel
from testit_api_client.models.work_item_states import WorkItemStates
from typing import Optional, Set
from typing_extensions import Self

class WorkItemPutModel(BaseModel):
    """
    WorkItemPutModel
    """ # noqa: E501
    attachments: List[AttachmentPutModel]
    iterations: Optional[List[IterationPutModel]] = None
    auto_tests: Optional[List[AutoTestIdModel]] = Field(default=None, alias="autoTests")
    id: StrictStr
    section_id: StrictStr = Field(alias="sectionId")
    description: Optional[StrictStr] = None
    state: WorkItemStates
    priority: WorkItemPriorityModel
    steps: List[StepPutModel]
    precondition_steps: List[StepPutModel] = Field(alias="preconditionSteps")
    postcondition_steps: List[StepPutModel] = Field(alias="postconditionSteps")
    duration: Annotated[int, Field(le=86400000, strict=True, ge=0)]
    attributes: Dict[str, Any]
    tags: List[TagPutModel]
    links: List[LinkPutModel]
    name: Annotated[str, Field(min_length=1, strict=True)]
    __properties: ClassVar[List[str]] = ["attachments", "iterations", "autoTests", "id", "sectionId", "description", "state", "priority", "steps", "preconditionSteps", "postconditionSteps", "duration", "attributes", "tags", "links", "name"]

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
        """Create an instance of WorkItemPutModel from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in iterations (list)
        _items = []
        if self.iterations:
            for _item_iterations in self.iterations:
                if _item_iterations:
                    _items.append(_item_iterations.to_dict())
            _dict['iterations'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in auto_tests (list)
        _items = []
        if self.auto_tests:
            for _item_auto_tests in self.auto_tests:
                if _item_auto_tests:
                    _items.append(_item_auto_tests.to_dict())
            _dict['autoTests'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in steps (list)
        _items = []
        if self.steps:
            for _item_steps in self.steps:
                if _item_steps:
                    _items.append(_item_steps.to_dict())
            _dict['steps'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in precondition_steps (list)
        _items = []
        if self.precondition_steps:
            for _item_precondition_steps in self.precondition_steps:
                if _item_precondition_steps:
                    _items.append(_item_precondition_steps.to_dict())
            _dict['preconditionSteps'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in postcondition_steps (list)
        _items = []
        if self.postcondition_steps:
            for _item_postcondition_steps in self.postcondition_steps:
                if _item_postcondition_steps:
                    _items.append(_item_postcondition_steps.to_dict())
            _dict['postconditionSteps'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in tags (list)
        _items = []
        if self.tags:
            for _item_tags in self.tags:
                if _item_tags:
                    _items.append(_item_tags.to_dict())
            _dict['tags'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in links (list)
        _items = []
        if self.links:
            for _item_links in self.links:
                if _item_links:
                    _items.append(_item_links.to_dict())
            _dict['links'] = _items
        # set to None if iterations (nullable) is None
        # and model_fields_set contains the field
        if self.iterations is None and "iterations" in self.model_fields_set:
            _dict['iterations'] = None

        # set to None if auto_tests (nullable) is None
        # and model_fields_set contains the field
        if self.auto_tests is None and "auto_tests" in self.model_fields_set:
            _dict['autoTests'] = None

        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict['description'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of WorkItemPutModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "attachments": [AttachmentPutModel.from_dict(_item) for _item in obj["attachments"]] if obj.get("attachments") is not None else None,
            "iterations": [IterationPutModel.from_dict(_item) for _item in obj["iterations"]] if obj.get("iterations") is not None else None,
            "autoTests": [AutoTestIdModel.from_dict(_item) for _item in obj["autoTests"]] if obj.get("autoTests") is not None else None,
            "id": obj.get("id"),
            "sectionId": obj.get("sectionId"),
            "description": obj.get("description"),
            "state": obj.get("state"),
            "priority": obj.get("priority"),
            "steps": [StepPutModel.from_dict(_item) for _item in obj["steps"]] if obj.get("steps") is not None else None,
            "preconditionSteps": [StepPutModel.from_dict(_item) for _item in obj["preconditionSteps"]] if obj.get("preconditionSteps") is not None else None,
            "postconditionSteps": [StepPutModel.from_dict(_item) for _item in obj["postconditionSteps"]] if obj.get("postconditionSteps") is not None else None,
            "duration": obj.get("duration"),
            "attributes": obj.get("attributes"),
            "tags": [TagPutModel.from_dict(_item) for _item in obj["tags"]] if obj.get("tags") is not None else None,
            "links": [LinkPutModel.from_dict(_item) for _item in obj["links"]] if obj.get("links") is not None else None,
            "name": obj.get("name")
        })
        return _obj


