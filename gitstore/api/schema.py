from enum import Enum
from fastapi import Body
from pydantic import BaseModel

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
    extra: dict = {}

class BatchRequest(BaseModel):
    operation: Operation
    transfers: list = Body(['basic'], embed=True)
    ref: Ref = None
    objects: list[Object]

class Actions(BaseModel):
    expires_in: int
    header: dict = None
    href: str

class ObjectActions(BaseModel):
    upload: Actions = None
    download: Actions = None

class ObjectResponse(BaseModel):
    transfer: str
    actions: ObjectActions
    authenticated: bool = True

