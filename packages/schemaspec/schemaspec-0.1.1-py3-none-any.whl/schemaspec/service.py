from dataclasses import dataclass
from typing import List


@dataclass
class HttpRoute:
    path: str
    method: str
    query_params: List[str]


@dataclass
class GrpcMethod:
    name: str


class ServiceMethod:
    def __init__(self, func):
        self.func = func
        self.http_route = None
        self.grpc_method = None

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.func.__get__(obj, objtype)


def http(path: str, method: str = "GET", query: List[str] = None):
    def decorator(func):
        if not isinstance(func, ServiceMethod):
            func = ServiceMethod(func)
        func.http_route = HttpRoute(path=path, method=method, query_params=query or [])
        return func

    return decorator


def grpc(name: str):
    def decorator(func):
        if not isinstance(func, ServiceMethod):
            func = ServiceMethod(func)
        func.grpc_method = GrpcMethod(name=name)
        return func

    return decorator


class Service:
    @classmethod
    def methods(cls):
        return {
            name: method
            for name, method in cls.__dict__.items()
            if isinstance(method, ServiceMethod)
        }
