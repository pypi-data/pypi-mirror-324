from schemaspec import Array, Enum, Integer, Schema, Service, String, grpc, http


class Pet(Schema):
    name = String(min_length=3, max_length=100, description="Pet's name")
    age = Integer(min_value=0, max_value=30, description="Pet's age in years")
    species = Enum(values=["dog", "cat", "bird"], description="Type of pet")
    tags = Array(items=String(max_length=20), description="Pet tags")


class ListPetsRequest(Schema):
    tag = String(description="Filter by tag")
    species = String(description="Filter by species")
    limit = Integer(min_value=1, max_value=100, default=10)


class ListPetsResponse(Schema):
    items = Array(items=Pet)
    total = Integer()


class PetService(Service):
    @http(path="/pets", method="GET", query=["tag", "species", "limit"])
    @grpc(name="ListPets")
    def list_pets(request: ListPetsRequest) -> ListPetsResponse:
        """List all pets with optional filtering"""
        pass


def test_service_method_metadata():
    methods = PetService.methods()
    assert "list_pets" in methods

    method = methods["list_pets"]
    assert method.http_route.path == "/pets"
    assert method.http_route.method == "GET"
    assert "tag" in method.http_route.query_params
    assert method.grpc_method.name == "ListPets"
