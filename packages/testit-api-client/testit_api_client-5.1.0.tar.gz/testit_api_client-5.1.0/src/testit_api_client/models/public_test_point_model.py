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
from testit_api_client.models.parameter_short_model import ParameterShortModel
from typing import Optional, Set
from typing_extensions import Self

class PublicTestPointModel(BaseModel):
    """
    PublicTestPointModel
    """ # noqa: E501
    configuration_id: StrictStr = Field(alias="configurationId")
    configuration_global_id: StrictInt = Field(alias="configurationGlobalId")
    auto_test_ids: Optional[List[StrictStr]] = Field(default=None, alias="autoTestIds")
    iteration_id: StrictStr = Field(alias="iterationId")
    parameter_models: Optional[List[ParameterShortModel]] = Field(default=None, alias="parameterModels")
    id: StrictStr
    __properties: ClassVar[List[str]] = ["configurationId", "configurationGlobalId", "autoTestIds", "iterationId", "parameterModels", "id"]

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
        """Create an instance of PublicTestPointModel from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in parameter_models (list)
        _items = []
        if self.parameter_models:
            for _item_parameter_models in self.parameter_models:
                if _item_parameter_models:
                    _items.append(_item_parameter_models.to_dict())
            _dict['parameterModels'] = _items
        # set to None if auto_test_ids (nullable) is None
        # and model_fields_set contains the field
        if self.auto_test_ids is None and "auto_test_ids" in self.model_fields_set:
            _dict['autoTestIds'] = None

        # set to None if parameter_models (nullable) is None
        # and model_fields_set contains the field
        if self.parameter_models is None and "parameter_models" in self.model_fields_set:
            _dict['parameterModels'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PublicTestPointModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "configurationId": obj.get("configurationId"),
            "configurationGlobalId": obj.get("configurationGlobalId"),
            "autoTestIds": obj.get("autoTestIds"),
            "iterationId": obj.get("iterationId"),
            "parameterModels": [ParameterShortModel.from_dict(_item) for _item in obj["parameterModels"]] if obj.get("parameterModels") is not None else None,
            "id": obj.get("id")
        })
        return _obj


