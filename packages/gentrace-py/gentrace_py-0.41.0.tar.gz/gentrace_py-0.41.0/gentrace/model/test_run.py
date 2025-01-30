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


class TestRun(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "createdAt",
            "resultId",
            "caseId",
            "id",
            "updatedAt",
        }
        
        class properties:
            id = schemas.UUIDSchema
            createdAt = schemas.StrSchema
            updatedAt = schemas.StrSchema
            caseId = schemas.UUIDSchema
            resultId = schemas.UUIDSchema
            
            
            class path(
                schemas.ListBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneTupleMixin
            ):
            
            
                class MetaOapg:
                    
                    @staticmethod
                    def items() -> typing.Type['RunPathSection']:
                        return RunPathSection
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[list, tuple, None, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'path':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            __annotations__ = {
                "id": id,
                "createdAt": createdAt,
                "updatedAt": updatedAt,
                "caseId": caseId,
                "resultId": resultId,
                "path": path,
            }
    
    createdAt: MetaOapg.properties.createdAt
    resultId: MetaOapg.properties.resultId
    caseId: MetaOapg.properties.caseId
    id: MetaOapg.properties.id
    updatedAt: MetaOapg.properties.updatedAt
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["createdAt"]) -> MetaOapg.properties.createdAt: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["updatedAt"]) -> MetaOapg.properties.updatedAt: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["caseId"]) -> MetaOapg.properties.caseId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["resultId"]) -> MetaOapg.properties.resultId: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["path"]) -> MetaOapg.properties.path: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["id", "createdAt", "updatedAt", "caseId", "resultId", "path", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["id"]) -> MetaOapg.properties.id: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["createdAt"]) -> MetaOapg.properties.createdAt: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["updatedAt"]) -> MetaOapg.properties.updatedAt: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["caseId"]) -> MetaOapg.properties.caseId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["resultId"]) -> MetaOapg.properties.resultId: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["path"]) -> typing.Union[MetaOapg.properties.path, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["id", "createdAt", "updatedAt", "caseId", "resultId", "path", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        createdAt: typing.Union[MetaOapg.properties.createdAt, str, ],
        resultId: typing.Union[MetaOapg.properties.resultId, str, uuid.UUID, ],
        caseId: typing.Union[MetaOapg.properties.caseId, str, uuid.UUID, ],
        id: typing.Union[MetaOapg.properties.id, str, uuid.UUID, ],
        updatedAt: typing.Union[MetaOapg.properties.updatedAt, str, ],
        path: typing.Union[MetaOapg.properties.path, list, tuple, None, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'TestRun':
        return super().__new__(
            cls,
            *_args,
            createdAt=createdAt,
            resultId=resultId,
            caseId=caseId,
            id=id,
            updatedAt=updatedAt,
            path=path,
            _configuration=_configuration,
            **kwargs,
        )

from gentrace.model.run_path_section import RunPathSection
