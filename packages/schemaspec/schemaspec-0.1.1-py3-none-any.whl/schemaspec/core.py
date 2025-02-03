from typing import Any, Dict, List, Type, Union

from pydantic import BaseModel, Field, field_validator
from pydantic._internal import _model_construction


class SchemaField:
    def __init__(self, **kwargs):
        self.kwargs = kwargs


class String(SchemaField):
    def __init__(
        self, min_length: int = None, max_length: int = None, description: str = None
    ):
        super().__init__(
            min_length=min_length, max_length=max_length, description=description
        )


class Integer(SchemaField):
    def __init__(
        self,
        min_value: int = None,
        max_value: int = None,
        description: str = None,
        default: int = None,
    ):
        super().__init__(
            ge=min_value, le=max_value, description=description, default=default
        )


class Array(SchemaField):
    def __init__(
        self,
        items: Union[SchemaField, Type[SchemaField]],
        description: str = None,
        default: List = None,
    ):
        self.items = items

        # Handle different item types
        if isinstance(items, type):
            if issubclass(items, Schema):
                # For Schema class, extract its model schema
                json_schema_extra = {"items": items.model_json_schema()}
            elif issubclass(items, SchemaField):
                # For SchemaField class, instantiate it
                items = items()
                json_schema_extra = {"items": items.kwargs}
        else:
            # For instances, use kwargs directly
            json_schema_extra = {"items": items.kwargs}
        # Handle default value
        if default is None:
            default = []  # Use empty list instead of list class
        super().__init__(
            description=description,
            json_schema_extra=json_schema_extra,
            default=default,
        )


class Enum(SchemaField):
    def __init__(self, values: List[str], description: str = None):
        super().__init__(description=description)
        self.values = values

    def get_validator(self):
        values = self.values  # Capture values in closure

        def validate(value: str) -> str:
            if value not in values:
                raise ValueError(f"Value must be one of {values}")
            return value

        return validate


class SchemaMeta(_model_construction.ModelMetaclass):
    def __new__(mcs, name, bases, namespace):
        annotations = namespace.get("__annotations__", {})
        fields = {}
        new_namespace = dict(namespace)  # Create a copy to avoid runtime modification

        # Collect field information first
        for key, value in namespace.items():
            if isinstance(value, SchemaField):
                if isinstance(value, String):
                    annotations[key] = str
                elif isinstance(value, Integer):
                    annotations[key] = int
                elif isinstance(value, Enum):
                    annotations[key] = str
                    new_namespace[f"validate_{key}"] = field_validator(key)(
                        value.get_validator()
                    )
                elif isinstance(value, Array):
                    annotations[key] = (
                        List[str] if isinstance(value.items, String) else List[Any]
                    )
                fields[key] = Field(**value.kwargs)

        new_namespace["__annotations__"] = annotations
        for key, value in fields.items():
            new_namespace[key] = value

        return super().__new__(mcs, name, bases, new_namespace)


class Schema(BaseModel, metaclass=SchemaMeta):
    @classmethod
    def parse(cls, data: Dict) -> "Schema":
        return cls(**data)

    @classmethod
    def parse_json(cls, json_str: str) -> "Schema":
        return cls.model_validate_json(json_str)

    def dict(self) -> Dict:
        return self.model_dump()

    def json(self) -> str:
        return self.model_dump_json()
