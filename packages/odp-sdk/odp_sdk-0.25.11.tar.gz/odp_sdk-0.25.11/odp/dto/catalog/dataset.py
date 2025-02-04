from typing import Any, Dict, List, Optional, Set

from pydantic import BaseModel, Field, root_validator, validator

from ..common.contact_info import ContactInfo
from ..resource import ResourceDto, ResourceSpec
from ..resource_registry import DEFAULT_RESOURCE_TYPE_REGISTRY
from ..validators import validate_doi


class Citation(BaseModel):
    """Citation information"""

    cite_as: Optional[str] = None
    """Directions on how to cite the dataset"""

    doi: Optional[str] = None

    @root_validator
    def _validate_creation(cls, values) -> "Citation":
        if not any(values.values()):
            raise ValueError(f"One of the fields must be set: {list(values.keys())}")

        return values

    @validator("doi")
    def _validate_doi(cls, value: str) -> str:
        if value:
            return validate_doi(value)
        return value


class Attribute(BaseModel):
    """Dataset attribute"""

    name: str
    """Attribute name. This can be a column name in a table, a dimension in an array, etc."""

    description: Optional[str] = None
    """Attribute description"""

    traits: list[str]
    """List of traits. Traits are used to describe the attribute in more detail.

    Traits are based on Microsoft Common Data Model (CDM) traits. See the [CDM documentation]
    (https://learn.microsoft.com/en-us/common-data-model/sdk/trait-concepts-and-use-cases#what-are-traits)
    for more information.
    """


class DatasetSpec(ResourceSpec):
    storage_class: str
    """Storage class qualified name"""

    storage_controller: Optional[str] = None
    """Storage controller qualified name"""

    data_collection: Optional[str] = None
    """Data collection qualified name"""

    maintainer: ContactInfo
    """Active maintainer information"""

    citation: Optional[Citation] = None
    """Citation information"""

    documentation: List[str] = Field(default_factory=list)
    """Links to any relevant documentation"""

    attributes: List[Attribute] = Field(default_factory=list)
    """Dataset attributes"""

    facets: Optional[Dict[str, Any]] = None
    """Facets for the dataset"""

    tags: Set[str] = Field(default_factory=set)


class DatasetDto(ResourceDto):
    _kind: str = "catalog.hubocean.io/dataset"
    _version: str = "v1alpha3"

    spec: DatasetSpec


DEFAULT_RESOURCE_TYPE_REGISTRY.add(DatasetDto)
