# coding: utf-8

"""
    Cisco Security Cloud Control API

    Use the documentation to explore the endpoints Security Cloud Control has to offer

    The version of the OpenAPI document: 1.5.0
    Contact: cdo.tac@cisco.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from cdo_sdk_python.models.application_context_class_loader_parent_unnamed_module_class_loader import ApplicationContextClassLoaderParentUnnamedModuleClassLoader
from cdo_sdk_python.models.application_context_class_loader_parent_unnamed_module_descriptor import ApplicationContextClassLoaderParentUnnamedModuleDescriptor
from typing import Optional, Set
from typing_extensions import Self

class ApplicationContextClassLoaderParentUnnamedModule(BaseModel):
    """
    ApplicationContextClassLoaderParentUnnamedModule
    """ # noqa: E501
    annotations: Optional[List[Dict[str, Any]]] = None
    class_loader: Optional[ApplicationContextClassLoaderParentUnnamedModuleClassLoader] = Field(default=None, alias="classLoader")
    declared_annotations: Optional[List[Dict[str, Any]]] = Field(default=None, alias="declaredAnnotations")
    descriptor: Optional[ApplicationContextClassLoaderParentUnnamedModuleDescriptor] = None
    layer: Optional[Dict[str, Any]] = None
    name: Optional[StrictStr] = None
    named: Optional[StrictBool] = None
    packages: Optional[List[StrictStr]] = None
    __properties: ClassVar[List[str]] = ["annotations", "classLoader", "declaredAnnotations", "descriptor", "layer", "name", "named", "packages"]

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
        """Create an instance of ApplicationContextClassLoaderParentUnnamedModule from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of class_loader
        if self.class_loader:
            _dict['classLoader'] = self.class_loader.to_dict()
        # override the default output from pydantic by calling `to_dict()` of descriptor
        if self.descriptor:
            _dict['descriptor'] = self.descriptor.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ApplicationContextClassLoaderParentUnnamedModule from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "annotations": obj.get("annotations"),
            "classLoader": ApplicationContextClassLoaderParentUnnamedModuleClassLoader.from_dict(obj["classLoader"]) if obj.get("classLoader") is not None else None,
            "declaredAnnotations": obj.get("declaredAnnotations"),
            "descriptor": ApplicationContextClassLoaderParentUnnamedModuleDescriptor.from_dict(obj["descriptor"]) if obj.get("descriptor") is not None else None,
            "layer": obj.get("layer"),
            "name": obj.get("name"),
            "named": obj.get("named"),
            "packages": obj.get("packages")
        })
        return _obj


