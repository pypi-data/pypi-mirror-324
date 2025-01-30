# coding: utf-8

"""
    FINBOURNE Candela Platform Web API

    FINBOURNE Technology  # noqa: E501

    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, Dict, List, Optional
from pydantic.v1 import BaseModel, conlist
from finbourne_candela.models.validation_error import ValidationError

class HTTPValidationError(BaseModel):
    """
    HTTPValidationError
    """
    detail: Optional[conlist(ValidationError)] = None
    additional_properties: Dict[str, Any] = {}
    __properties = ["detail"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def __str__(self):
        """For `print` and `pprint`"""
        return pprint.pformat(self.dict(by_alias=False))

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> HTTPValidationError:
        """Create an instance of HTTPValidationError from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in detail (list)
        _items = []
        if self.detail:
            for _item in self.detail:
                if _item:
                    _items.append(_item.to_dict())
            _dict['detail'] = _items
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> HTTPValidationError:
        """Create an instance of HTTPValidationError from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return HTTPValidationError.parse_obj(obj)

        _obj = HTTPValidationError.parse_obj({
            "detail": [ValidationError.from_dict(_item) for _item in obj.get("detail")] if obj.get("detail") is not None else None
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj
