# coding: utf-8

"""
    Arthur Scope

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from scope_client.api_bindings.models.alert_bound import AlertBound
from typing import Optional, Set
from typing_extensions import Self

class PostAlertRule(BaseModel):
    """
    PostAlertRule
    """ # noqa: E501
    name: StrictStr = Field(description="The name of the alert rule.")
    description: Optional[StrictStr] = None
    threshold: Union[StrictFloat, StrictInt] = Field(description="The threshold that will trigger the alert rule.")
    bound: AlertBound = Field(description="The bound of the alert rule.")
    query: StrictStr = Field(description="The query of the alert rule.")
    metric_name: StrictStr = Field(description="The name of the metric returned by the alert rule query.")
    notification_webhook_ids: Optional[List[StrictStr]] = Field(default=None, description="The notification webhook IDs where the alert rule will send alert notification.")
    __properties: ClassVar[List[str]] = ["name", "description", "threshold", "bound", "query", "metric_name", "notification_webhook_ids"]

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
        """Create an instance of PostAlertRule from a JSON string"""
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
        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict['description'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PostAlertRule from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "description": obj.get("description"),
            "threshold": obj.get("threshold"),
            "bound": obj.get("bound"),
            "query": obj.get("query"),
            "metric_name": obj.get("metric_name"),
            "notification_webhook_ids": obj.get("notification_webhook_ids")
        })
        return _obj


