I want to develop a Python framework to describe schemas concisely. You will help me to develop it.

Some requirements:

- Use Pydantic v2 (latest)
- Hide all Pydantic things to expose a simple to use primitives for describing schemas
- Tests are provided

I expect users can use the framework like this

```python
# schemaspec is my package
from schemaspec import (
    Schema,
    String,
    Integer,
    Enum,
    Array,
)


class Pet(Schema):
    name = String(min_length=3, max_length=100, description="Pet's name")
    age = Integer(min_value=0, max_value=30, description="Pet's age in years")
    species = Enum(values=["dog", "cat", "bird"], description="Type of pet")
    tags = Array(items=String(max_length=20), description="Pet tags")

# usages
pet = Pet(name="Buddy", age=5, species="dog", tags=["friendly", "trained"])
print(pet.name)
pet_data = {"name": "Max", "age": 3, "species": "cat", "tags": ["indoor"]}
pet = Pet.parse(pet_data)

json_str = '{"name": "Luna", "age": 2, "species": "bird", "tags": ["singer"]}'
pet = Pet.parse_json(json_str)
```
