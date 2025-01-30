"""
Type annotations for notificationscontacts service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_notificationscontacts/type_defs/)

Usage::

    ```python
    from types_boto3_notificationscontacts.type_defs import ActivateEmailContactRequestRequestTypeDef

    data: ActivateEmailContactRequestRequestTypeDef = ...
    ```

Copyright 2025 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime

from .literals import EmailContactStatusType

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import list as List
    from collections.abc import Mapping, Sequence
else:
    from typing import Dict, List, Mapping, Sequence
if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict


__all__ = (
    "ActivateEmailContactRequestRequestTypeDef",
    "CreateEmailContactRequestRequestTypeDef",
    "CreateEmailContactResponseTypeDef",
    "DeleteEmailContactRequestRequestTypeDef",
    "EmailContactTypeDef",
    "GetEmailContactRequestRequestTypeDef",
    "GetEmailContactResponseTypeDef",
    "ListEmailContactsRequestPaginateTypeDef",
    "ListEmailContactsRequestRequestTypeDef",
    "ListEmailContactsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "ResponseMetadataTypeDef",
    "SendActivationCodeRequestRequestTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
)


class ActivateEmailContactRequestRequestTypeDef(TypedDict):
    arn: str
    code: str


class CreateEmailContactRequestRequestTypeDef(TypedDict):
    name: str
    emailAddress: str
    tags: NotRequired[Mapping[str, str]]


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class DeleteEmailContactRequestRequestTypeDef(TypedDict):
    arn: str


class EmailContactTypeDef(TypedDict):
    arn: str
    name: str
    address: str
    status: EmailContactStatusType
    creationTime: datetime
    updateTime: datetime


class GetEmailContactRequestRequestTypeDef(TypedDict):
    arn: str


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class ListEmailContactsRequestRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    arn: str


class SendActivationCodeRequestRequestTypeDef(TypedDict):
    arn: str


class TagResourceRequestRequestTypeDef(TypedDict):
    arn: str
    tags: Mapping[str, str]


class UntagResourceRequestRequestTypeDef(TypedDict):
    arn: str
    tagKeys: Sequence[str]


class CreateEmailContactResponseTypeDef(TypedDict):
    arn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class GetEmailContactResponseTypeDef(TypedDict):
    emailContact: EmailContactTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListEmailContactsResponseTypeDef(TypedDict):
    emailContacts: List[EmailContactTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListEmailContactsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]
