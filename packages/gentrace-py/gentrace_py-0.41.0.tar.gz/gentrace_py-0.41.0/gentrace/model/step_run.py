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


class StepRun(
    schemas.DictSchema
):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """


    class MetaOapg:
        required = {
            "outputs",
            "invocation",
            "modelParams",
            "inputs",
            "startTime",
            "endTime",
            "providerName",
            "elapsedTime",
        }
        
        class properties:
            providerName = schemas.StrSchema
            invocation = schemas.StrSchema
            
            
            class modelParams(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    additional_properties = schemas.AnyTypeSchema
                
                def __getitem__(self, name: typing.Union[str, ]) -> MetaOapg.additional_properties:
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                def get_item_oapg(self, name: typing.Union[str, ]) -> MetaOapg.additional_properties:
                    return super().get_item_oapg(name)
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[MetaOapg.additional_properties, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                ) -> 'modelParams':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class inputs(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    additional_properties = schemas.AnyTypeSchema
                
                def __getitem__(self, name: typing.Union[str, ]) -> MetaOapg.additional_properties:
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                def get_item_oapg(self, name: typing.Union[str, ]) -> MetaOapg.additional_properties:
                    return super().get_item_oapg(name)
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[MetaOapg.additional_properties, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                ) -> 'inputs':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class outputs(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    additional_properties = schemas.AnyTypeSchema
                
                def __getitem__(self, name: typing.Union[str, ]) -> MetaOapg.additional_properties:
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                def get_item_oapg(self, name: typing.Union[str, ]) -> MetaOapg.additional_properties:
                    return super().get_item_oapg(name)
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[MetaOapg.additional_properties, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader, ],
                ) -> 'outputs':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                        **kwargs,
                    )
            elapsedTime = schemas.IntSchema
            startTime = schemas.DateTimeSchema
            endTime = schemas.DateTimeSchema
            
            
            class context(
                schemas.DictSchema
            ):
            
            
                class MetaOapg:
                    
                    class properties:
                        userId = schemas.StrSchema
                        
                        
                        class render(
                            schemas.DictSchema
                        ):
                        
                        
                            class MetaOapg:
                                required = {
                                    "type",
                                }
                                
                                class properties:
                                    type = schemas.StrSchema
                                    key = schemas.StrSchema
                                    __annotations__ = {
                                        "type": type,
                                        "key": key,
                                    }
                            
                            type: MetaOapg.properties.type
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
                            
                            @typing.overload
                            def __getitem__(self, name: typing_extensions.Literal["key"]) -> MetaOapg.properties.key: ...
                            
                            @typing.overload
                            def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                            
                            def __getitem__(self, name: typing.Union[typing_extensions.Literal["type", "key", ], str]):
                                # dict_instance[name] accessor
                                return super().__getitem__(name)
                            
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["type"]) -> MetaOapg.properties.type: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: typing_extensions.Literal["key"]) -> typing.Union[MetaOapg.properties.key, schemas.Unset]: ...
                            
                            @typing.overload
                            def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                            
                            def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["type", "key", ], str]):
                                return super().get_item_oapg(name)
                            
                        
                            def __new__(
                                cls,
                                *_args: typing.Union[dict, frozendict.frozendict, ],
                                type: typing.Union[MetaOapg.properties.type, str, ],
                                key: typing.Union[MetaOapg.properties.key, str, schemas.Unset] = schemas.unset,
                                _configuration: typing.Optional[schemas.Configuration] = None,
                                **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                            ) -> 'render':
                                return super().__new__(
                                    cls,
                                    *_args,
                                    type=type,
                                    key=key,
                                    _configuration=_configuration,
                                    **kwargs,
                                )
                        
                        
                        class metadata(
                            schemas.DictBase,
                            schemas.NoneBase,
                            schemas.Schema,
                            schemas.NoneFrozenDictMixin
                        ):
                        
                        
                            class MetaOapg:
                                
                                @staticmethod
                                def additional_properties() -> typing.Type['MetadataValueObject']:
                                    return MetadataValueObject
                        
                            
                            def __getitem__(self, name: typing.Union[str, ]) -> 'MetadataValueObject':
                                # dict_instance[name] accessor
                                return super().__getitem__(name)
                            
                            def get_item_oapg(self, name: typing.Union[str, ]) -> 'MetadataValueObject':
                                return super().get_item_oapg(name)
                        
                            def __new__(
                                cls,
                                *_args: typing.Union[dict, frozendict.frozendict, None, ],
                                _configuration: typing.Optional[schemas.Configuration] = None,
                                **kwargs: 'MetadataValueObject',
                            ) -> 'metadata':
                                return super().__new__(
                                    cls,
                                    *_args,
                                    _configuration=_configuration,
                                    **kwargs,
                                )
                        __annotations__ = {
                            "userId": userId,
                            "render": render,
                            "metadata": metadata,
                        }
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["userId"]) -> MetaOapg.properties.userId: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["render"]) -> MetaOapg.properties.render: ...
                
                @typing.overload
                def __getitem__(self, name: typing_extensions.Literal["metadata"]) -> MetaOapg.properties.metadata: ...
                
                @typing.overload
                def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
                
                def __getitem__(self, name: typing.Union[typing_extensions.Literal["userId", "render", "metadata", ], str]):
                    # dict_instance[name] accessor
                    return super().__getitem__(name)
                
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["userId"]) -> typing.Union[MetaOapg.properties.userId, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["render"]) -> typing.Union[MetaOapg.properties.render, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: typing_extensions.Literal["metadata"]) -> typing.Union[MetaOapg.properties.metadata, schemas.Unset]: ...
                
                @typing.overload
                def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
                
                def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["userId", "render", "metadata", ], str]):
                    return super().get_item_oapg(name)
                
            
                def __new__(
                    cls,
                    *_args: typing.Union[dict, frozendict.frozendict, ],
                    userId: typing.Union[MetaOapg.properties.userId, str, schemas.Unset] = schemas.unset,
                    render: typing.Union[MetaOapg.properties.render, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
                    metadata: typing.Union[MetaOapg.properties.metadata, dict, frozendict.frozendict, None, schemas.Unset] = schemas.unset,
                    _configuration: typing.Optional[schemas.Configuration] = None,
                    **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
                ) -> 'context':
                    return super().__new__(
                        cls,
                        *_args,
                        userId=userId,
                        render=render,
                        metadata=metadata,
                        _configuration=_configuration,
                        **kwargs,
                    )
            
            
            class error(
                schemas.StrBase,
                schemas.NoneBase,
                schemas.Schema,
                schemas.NoneStrMixin
            ):
            
            
                def __new__(
                    cls,
                    *_args: typing.Union[None, str, ],
                    _configuration: typing.Optional[schemas.Configuration] = None,
                ) -> 'error':
                    return super().__new__(
                        cls,
                        *_args,
                        _configuration=_configuration,
                    )
            __annotations__ = {
                "providerName": providerName,
                "invocation": invocation,
                "modelParams": modelParams,
                "inputs": inputs,
                "outputs": outputs,
                "elapsedTime": elapsedTime,
                "startTime": startTime,
                "endTime": endTime,
                "context": context,
                "error": error,
            }
    
    outputs: MetaOapg.properties.outputs
    invocation: MetaOapg.properties.invocation
    modelParams: MetaOapg.properties.modelParams
    inputs: MetaOapg.properties.inputs
    startTime: MetaOapg.properties.startTime
    endTime: MetaOapg.properties.endTime
    providerName: MetaOapg.properties.providerName
    elapsedTime: MetaOapg.properties.elapsedTime
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["providerName"]) -> MetaOapg.properties.providerName: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["invocation"]) -> MetaOapg.properties.invocation: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["modelParams"]) -> MetaOapg.properties.modelParams: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["inputs"]) -> MetaOapg.properties.inputs: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["outputs"]) -> MetaOapg.properties.outputs: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["elapsedTime"]) -> MetaOapg.properties.elapsedTime: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["startTime"]) -> MetaOapg.properties.startTime: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["endTime"]) -> MetaOapg.properties.endTime: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["context"]) -> MetaOapg.properties.context: ...
    
    @typing.overload
    def __getitem__(self, name: typing_extensions.Literal["error"]) -> MetaOapg.properties.error: ...
    
    @typing.overload
    def __getitem__(self, name: str) -> schemas.UnsetAnyTypeSchema: ...
    
    def __getitem__(self, name: typing.Union[typing_extensions.Literal["providerName", "invocation", "modelParams", "inputs", "outputs", "elapsedTime", "startTime", "endTime", "context", "error", ], str]):
        # dict_instance[name] accessor
        return super().__getitem__(name)
    
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["providerName"]) -> MetaOapg.properties.providerName: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["invocation"]) -> MetaOapg.properties.invocation: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["modelParams"]) -> MetaOapg.properties.modelParams: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["inputs"]) -> MetaOapg.properties.inputs: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["outputs"]) -> MetaOapg.properties.outputs: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["elapsedTime"]) -> MetaOapg.properties.elapsedTime: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["startTime"]) -> MetaOapg.properties.startTime: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["endTime"]) -> MetaOapg.properties.endTime: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["context"]) -> typing.Union[MetaOapg.properties.context, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: typing_extensions.Literal["error"]) -> typing.Union[MetaOapg.properties.error, schemas.Unset]: ...
    
    @typing.overload
    def get_item_oapg(self, name: str) -> typing.Union[schemas.UnsetAnyTypeSchema, schemas.Unset]: ...
    
    def get_item_oapg(self, name: typing.Union[typing_extensions.Literal["providerName", "invocation", "modelParams", "inputs", "outputs", "elapsedTime", "startTime", "endTime", "context", "error", ], str]):
        return super().get_item_oapg(name)
    

    def __new__(
        cls,
        *_args: typing.Union[dict, frozendict.frozendict, ],
        outputs: typing.Union[MetaOapg.properties.outputs, dict, frozendict.frozendict, ],
        invocation: typing.Union[MetaOapg.properties.invocation, str, ],
        modelParams: typing.Union[MetaOapg.properties.modelParams, dict, frozendict.frozendict, ],
        inputs: typing.Union[MetaOapg.properties.inputs, dict, frozendict.frozendict, ],
        startTime: typing.Union[MetaOapg.properties.startTime, str, datetime, ],
        endTime: typing.Union[MetaOapg.properties.endTime, str, datetime, ],
        providerName: typing.Union[MetaOapg.properties.providerName, str, ],
        elapsedTime: typing.Union[MetaOapg.properties.elapsedTime, decimal.Decimal, int, ],
        context: typing.Union[MetaOapg.properties.context, dict, frozendict.frozendict, schemas.Unset] = schemas.unset,
        error: typing.Union[MetaOapg.properties.error, None, str, schemas.Unset] = schemas.unset,
        _configuration: typing.Optional[schemas.Configuration] = None,
        **kwargs: typing.Union[schemas.AnyTypeSchema, dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, None, list, tuple, bytes],
    ) -> 'StepRun':
        return super().__new__(
            cls,
            *_args,
            outputs=outputs,
            invocation=invocation,
            modelParams=modelParams,
            inputs=inputs,
            startTime=startTime,
            endTime=endTime,
            providerName=providerName,
            elapsedTime=elapsedTime,
            context=context,
            error=error,
            _configuration=_configuration,
            **kwargs,
        )

from gentrace.model.metadata_value_object import MetadataValueObject
