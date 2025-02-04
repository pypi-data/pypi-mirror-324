from typing import Any, Dict

import jsonschema
from pydantic import validator

from ..resource import ResourceDto, ResourceSpec
from ..resource_registry import DEFAULT_RESOURCE_TYPE_REGISTRY


class ObservableClassSpec(ResourceSpec):
    observable_schema: Dict
    """JSON Schema for the observable class"""

    @validator("observable_schema", pre=True, always=True)
    def validate_json_schema(cls, v: Any) -> Any:
        try:
            jsonschema.Draft4Validator.check_schema(v)
        except jsonschema.SchemaError as e:
            raise ValueError(f"Schema is invalid: {e.message}") from e
        return v

    def validate_dict(self, d: Dict[str, Any]):
        try:
            jsonschema.validate(instance=d, schema=self.observable_schema)
        except jsonschema.ValidationError as e:
            raise ValueError(f"Observable details do not match schema: {e.message}") from e


class ObservableClassDto(ResourceDto):
    _kind: str = "catalog.hubocean.io/observableClass"
    _version: str = "v1alpha1"

    spec: ObservableClassSpec


DEFAULT_RESOURCE_TYPE_REGISTRY.add(ObservableClassDto)
