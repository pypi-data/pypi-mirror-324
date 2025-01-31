from geojson_pydantic import Feature

from odp.dto import MetadataDto
from odp.dto.registry import ObservableClassDto, ObservableClassSpec

static_single_value_class = ObservableClassDto(
    metadata=MetadataDto(
        name="static-observable",
        labels={"catalog.hubocean.io/released": True},
    ),
    spec=ObservableClassSpec(
        observable_schema={
            "$schema": "http://json-schema.org/draft-04/schema#",
            "title": "StaticObservable",
            "type": "object",
            "description": "Single value observable",
            "properties": {"attribute": {"title": "Attribute", "type": "string"}, "value": {"title": "Value"}},
            "required": ["value"],
        }
    ),
)


static_coverage_class = ObservableClassDto(
    metadata=MetadataDto(
        name="static-coverage",
        labels={"catalog.hubocean.io/released": True},
    ),
    spec=ObservableClassSpec(
        observable_schema={
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object",
            "title": "StaticCoverage",
            "description": "1D real coverage",
            "required": ["attribute", "value"],
            "properties": {
                "value": {
                    "type": "array",
                    "items": [{"type": "number"}, {"type": "number"}],
                    "title": "Value",
                    "maxItems": 2,
                    "minItems": 2,
                },
                "attribute": {"type": "string", "title": "Attribute"},
            },
        }
    ),
)

static_geometric_coverage_class = ObservableClassDto(
    metadata=MetadataDto(
        name="static-geometric-coverage",
        labels={"catalog.hubocean.io/released": True},
    ),
    spec=ObservableClassSpec(
        observable_schema={
            "$schema": "http://json-schema.org/draft-04/schema#",
            "title": "StaticGeometricCoverage",
            "description": "Geometric coverage",
            "type": "object",
            "required": ["attribute", "value"],
            "properties": {
                "attribute": {"title": "Attribute", "type": "string"},
                "value": {"$ref": "#/definitions/Feature"},
            },
            "definitions": (lambda schema: {**schema.pop("definitions"), "Feature": schema})(Feature.schema()),
        }
    ),
)
