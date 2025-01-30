# coding: utf-8

"""
    Gentrace API

    These API routes are designed to ingest events from clients.  # noqa: E501

    The version of the OpenAPI document: 0.27.0
    Generated by: https://openapi-generator.tech
"""

from datetime import date, datetime  # noqa: F401
import decimal  # noqa: F401
import functools  # noqa: F401
import io  # noqa: F401
import re  # noqa: F401
import typing  # noqa: F401
import typing_extensions  # noqa: F401
import uuid  # noqa: F401

import frozendict  # noqa: F401

from gentrace import schemas  # noqa: F401


class FolderV2(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "organizationId",
            "createdAt",
            "parentFolderId",
            "name",
            "id",
            "updatedAt",
        }
        
        class properties:
            id = schemas.UUIDSchema
            createdAt = schemas.Float32Schema
            updatedAt = schemas.Float32Schema
            name = schemas.StrSchema
            organizationId = schemas.UUIDSchema
            
            
            class parentFolderId(
                schemas.UUIDBase,
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                class MetaOapg:
                    format = 'uuid'
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, uuid.UUID, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'parentFolderId':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            __annotations__ = {
                "id": id,
                "createdAt": createdAt,
                "updatedAt": updatedAt,
                "name": name,
                "organizationId": organizationId,
                "parentFolderId": parentFolderId,
            }
    
    organizationId: MetaOapg.properties.organizationId
    createdAt: MetaOapg.properties.createdAt
    parentFolderId: MetaOapg.properties.parentFolderId
    name: MetaOapg.properties.name
    id: MetaOapg.properties.id
    updatedAt: MetaOapg.properties.updatedAt
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["createdAt"]) -> MetaOapg.properties.createdAt: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["updatedAt"]) -> MetaOapg.properties.updatedAt: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["organizationId"]) -> MetaOapg.properties.organizationId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["parentFolderId"]) -> MetaOapg.properties.parentFolderId: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["id", "createdAt", "updatedAt", "name", "organizationId", "parentFolderId", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["createdAt"]) -> MetaOapg.properties.createdAt: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["updatedAt"]) -> MetaOapg.properties.updatedAt: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["name"]) -> MetaOapg.properties.name: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["organizationId"]) -> MetaOapg.properties.organizationId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["parentFolderId"]) -> MetaOapg.properties.parentFolderId: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id", "createdAt", "updatedAt", "name", "organizationId", "parentFolderId", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        organizationId: typing.Union[MetaOapg.properties.organizationId, str, uuid.UUID, ],
        createdAt: typing.Union[MetaOapg.properties.createdAt, decimal.Decimal, int, float, ],
        parentFolderId: typing.Union[MetaOapg.properties.parentFolderId, None, str, uuid.UUID, ],
        name: typing.Union[MetaOapg.properties.name, str, ],
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, ],
        updatedAt: typing.Union[MetaOapg.properties.updatedAt, decimal.Decimal, int, float, ],
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'FolderV2':
        return super().__new__(
            cls,
            *_args,
            organizationId=organizationId,
            createdAt=createdAt,
            parentFolderId=parentFolderId,
            name=name,
            id=id,
            updatedAt=updatedAt,
            _configuration=_configuration,
            **kwargs,
        )
