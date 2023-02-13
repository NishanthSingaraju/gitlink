from enum import Enum
from fastapi import Body
from pydantic import BaseModel
from typing import List

class Operation(str, Enum):
    """Batch operations"""
    upload = 'upload'
    download = 'download'

class Ref(BaseModel):
    """ref field model"""
    name: str

class Object(BaseModel):
    """object field mode"""
    oid: str
    size: int

class BatchRequest(BaseModel):
    operation: Operation
    transfers: list = Body(['basic'], embed=True)
    ref: Ref = None
    objects: list[Object]


class ObjectResponse(BaseModel):
    oid: str
    size: int
    actions: dict
