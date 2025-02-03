# SchemaSpec

A schema-first Python library inspired by TypeSpec for defining data models and APIs with strong typing and validation.

## Features

- 📝 Schema-first approach to model definition
- 💪 Strong typing with runtime validation
- 🔍 Clear and explicit field validation
- 📚 Built-in documentation support
- 🔄 OpenAPI generation
- 🧩 Extensible type system
- ⚡ High performance using Pydantic under the hood
- 🔒 Immutable models by default

## Installation

```bash
pip install schemaspec
```

For development installation:

```bash
pip install schemaspec[dev]
```

## Quick Start

```python
from schemaspec import Schema, String, Integer, Enum, Array

# Define a schema
class Pet(Schema):
    name=String(
        min_length=3,
        max_length=100,
        description="Pet's name"
    ),
    age=Integer(
        min_value=0,
        max_value=30,
        description="Pet's age in years"
    ),
    species=Enum(
        values=["dog", "cat", "bird"],
        description="Type of pet"
    ),
    tags=Array(
        items=String(max_length=20),
        description="Pet tags"
    )
)

# Create an instance
pet = Pet(
    name="Buddy",
    age=5,
    species="dog",
    tags=["friendly", "trained"]
)

# Convert to dictionary
pet_dict = pet.dict()

# Convert to JSON
pet_json = pet.json()

# Parse from dictionary
pet2 = Pet.parse({
    "name": "Max",
    "age": 3,
    "species": "cat",
    "tags": ["indoor"]
})

# Parse from JSON
json_str = '{"name": "Luna", "age": 2, "species": "bird", "tags": ["singer"]}'
pet3 = Pet.parse_json(json_str)
```

## Available Types

- `String`: Text data with optional length and pattern validation
- `Integer`: Whole numbers with optional range validation
- `Float`: Decimal numbers with optional range validation
- `Enum`: Fixed set of allowed values
- `Array`: List of items of a specific type
- More types coming soon!

## Development

### Prerequisites

- Python 3.8+
- [just](https://github.com/casey/just) command runner

### Setting Up Development Environment

```bash
# List all available commands
just

# Setup complete development environment
just bootstrap

# Run tests
just test

# Format code
just fmt

# Run linting
just lint

# Run all checks
just check
```

### Common Development Tasks

```bash
# Install development dependencies
just dev

# Serve documentation
just serve-docs

# Watch tests
just watch

# Run security checks
just security
```

### Available Just Commands

| Command           | Description                            |
| ----------------- | -------------------------------------- |
| `just`            | List all available commands            |
| `just bootstrap`  | Setup complete development environment |
| `just dev`        | Install development dependencies       |
| `just test`       | Run tests                              |
| `just test-cov`   | Run tests with coverage                |
| `just fmt`        | Format code                            |
| `just lint`       | Run linting                            |
| `just check`      | Run all checks                         |
| `just serve-docs` | Serve documentation                    |
| `just build-docs` | Build documentation                    |
| `just clean`      | Clean build artifacts                  |
| `just security`   | Run security checks                    |

## API Documentation

### Defining Schemas

```python
from schemaspec import Schema, String, Integer

class User(Schema):
    username=String(
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Username (alphanumeric and underscore)"
    ),
    age=Integer(
        min_value=0,
        max_value=150,
        description="User age in years"
    )
)
```

### API Decorators

```python
from schemaspec import Schema, String, Integer, Enum, Array, service, server, route

# Define a schema
class Pet(Schema):
    name=String(
        min_length=3,
        max_length=100,
        description="Pet's name"
    ),
    age=Integer(
        min_value=0,
        max_value=30,
        description="Pet's age in years"
    ),
    species=Enum(
        values=["dog", "cat", "bird"],
        description="Type of pet"
    ),
    tags=Array(
        items=String(max_length=20),
        description="Pet tags"
    )
)

@service(title="Pet Store Service", version="1.0.0")
@server("https://api.petstore.com/v1", "Production API")
class PetService:
    @route("/pets", methods=["GET"], tags=["pets"])
    def list() -> Array(items=Pet):    
        pass
```

## Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

### Development Workflow

1. Fork the repository
2. Setup development environment: `just bootstrap`
3. Make your changes
4. Run checks: `just check`
5. Submit a Pull Request

## License

MIT

## Credits

- Inspired by [TypeSpec](https://typespec.io/)
- Powered by [Pydantic](https://pydantic-docs.helpmanual.io/)
