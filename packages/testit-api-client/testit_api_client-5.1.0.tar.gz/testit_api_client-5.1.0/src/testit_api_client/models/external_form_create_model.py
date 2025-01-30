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
from typing import Any, ClassVar, Dict, List
from testit_api_client.models.external_form_allowed_value_model import ExternalFormAllowedValueModel
from testit_api_client.models.external_form_field_model import ExternalFormFieldModel
from testit_api_client.models.external_form_link_model import ExternalFormLinkModel
from typing import Optional, Set
from typing_extensions import Self

class ExternalFormCreateModel(BaseModel):
    """
    ExternalFormCreateModel
    """ # noqa: E501
    possible_values: Dict[str, List[ExternalFormAllowedValueModel]] = Field(alias="possibleValues")
    fields: List[ExternalFormFieldModel]
    links: List[ExternalFormLinkModel]
    values: Dict[str, Any]
    __properties: ClassVar[List[str]] = ["possibleValues", "fields", "links", "values"]

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
        """Create an instance of ExternalFormCreateModel from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each value in possible_values (dict of array)
        _field_dict_of_array = {}
        if self.possible_values:
            for _key_possible_values in self.possible_values:
                if self.possible_values[_key_possible_values] is not None:
                    _field_dict_of_array[_key_possible_values] = [
                        _item.to_dict() for _item in self.possible_values[_key_possible_values]
                    ]
            _dict['possibleValues'] = _field_dict_of_array
        # override the default output from pydantic by calling `to_dict()` of each item in fields (list)
        _items = []
        if self.fields:
            for _item_fields in self.fields:
                if _item_fields:
                    _items.append(_item_fields.to_dict())
            _dict['fields'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in links (list)
        _items = []
        if self.links:
            for _item_links in self.links:
                if _item_links:
                    _items.append(_item_links.to_dict())
            _dict['links'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ExternalFormCreateModel from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "possibleValues": dict(
                (_k,
                        [ExternalFormAllowedValueModel.from_dict(_item) for _item in _v]
                        if _v is not None
                        else None
                )
                for _k, _v in obj.get("possibleValues", {}).items()
            ),
            "fields": [ExternalFormFieldModel.from_dict(_item) for _item in obj["fields"]] if obj.get("fields") is not None else None,
            "links": [ExternalFormLinkModel.from_dict(_item) for _item in obj["links"]] if obj.get("links") is not None else None,
            "values": obj.get("values")
        })
        return _obj


