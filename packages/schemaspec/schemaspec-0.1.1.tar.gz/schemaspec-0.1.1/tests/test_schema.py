import json

import pytest

from schemaspec import Array, Enum, Integer, Schema, String


class Pet(Schema):
    name = String(min_length=3, max_length=100, description="Pet's name")
    age = Integer(min_value=0, max_value=30, description="Pet's age in years")
    species = Enum(values=["dog", "cat", "bird"], description="Type of pet")
    tags = Array(items=String(max_length=20), description="Pet tags")


def test_pet_direct_instantiation():
    pet = Pet(name="Buddy", age=5, species="dog", tags=["friendly", "trained"])
    assert pet.name == "Buddy"
    assert pet.age == 5
    assert pet.species == "dog"
    assert pet.tags == ["friendly", "trained"]


def test_pet_parse_dict():
    pet_data = {"name": "Max", "age": 3, "species": "cat", "tags": ["indoor"]}
    pet = Pet.parse(pet_data)
    assert pet.name == "Max"
    assert pet.age == 3
    assert pet.species == "cat"
    assert pet.tags == ["indoor"]


def test_pet_parse_json():
    json_str = '{"name": "Luna", "age": 2, "species": "bird", "tags": ["singer"]}'
    pet = Pet.parse_json(json_str)
    assert pet.name == "Luna"
    assert pet.age == 2
    assert pet.species == "bird"
    assert pet.tags == ["singer"]


def test_pet_validation_name_length():
    with pytest.raises(Exception):
        Pet(name="Bo", age=5, species="dog", tags=["friendly"])


def test_pet_validation_age_range():
    with pytest.raises(Exception):
        Pet(name="Buddy", age=31, species="dog", tags=["friendly"])


def test_pet_validation_species_enum():
    with pytest.raises(Exception):
        Pet(name="Buddy", age=5, species="hamster", tags=["friendly"])


def test_pet_to_dict():
    pet = Pet(name="Buddy", age=5, species="dog", tags=["friendly", "trained"])

    pet_dict = pet.dict()
    assert pet_dict == {
        "name": "Buddy",
        "age": 5,
        "species": "dog",
        "tags": ["friendly", "trained"],
    }


def test_pet_to_json():
    pet = Pet(name="Buddy", age=5, species="dog", tags=["friendly", "trained"])
    pet_json = pet.json()
    assert json.loads(pet_json) == {
        "name": "Buddy",
        "age": 5,
        "species": "dog",
        "tags": ["friendly", "trained"],
    }
