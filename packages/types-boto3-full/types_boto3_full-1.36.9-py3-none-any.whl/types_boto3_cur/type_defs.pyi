"""
Type annotations for cur service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_cur/type_defs/)

Usage::

    ```python
    from types_boto3_cur.type_defs import DeleteReportDefinitionRequestRequestTypeDef

    data: DeleteReportDefinitionRequestRequestTypeDef = ...
    ```

Copyright 2025 Vlad Emelianov
"""

from __future__ import annotations

import sys

from .literals import (
    AdditionalArtifactType,
    AWSRegionType,
    CompressionFormatType,
    LastStatusType,
    ReportFormatType,
    ReportVersioningType,
    SchemaElementType,
    TimeUnitType,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import list as List
    from collections.abc import Sequence
else:
    from typing import Dict, List, Sequence
if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "DeleteReportDefinitionRequestRequestTypeDef",
    "DeleteReportDefinitionResponseTypeDef",
    "DescribeReportDefinitionsRequestPaginateTypeDef",
    "DescribeReportDefinitionsRequestRequestTypeDef",
    "DescribeReportDefinitionsResponseTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ModifyReportDefinitionRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "PutReportDefinitionRequestRequestTypeDef",
    "ReportDefinitionOutputTypeDef",
    "ReportDefinitionTypeDef",
    "ReportStatusTypeDef",
    "ResponseMetadataTypeDef",
    "TagResourceRequestRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestRequestTypeDef",
)

class DeleteReportDefinitionRequestRequestTypeDef(TypedDict):
    ReportName: str

class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]

class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]

class DescribeReportDefinitionsRequestRequestTypeDef(TypedDict):
    MaxResults: NotRequired[int]
    NextToken: NotRequired[str]

class ListTagsForResourceRequestRequestTypeDef(TypedDict):
    ReportName: str

class TagTypeDef(TypedDict):
    Key: str
    Value: str

class ReportStatusTypeDef(TypedDict):
    lastDelivery: NotRequired[str]
    lastStatus: NotRequired[LastStatusType]

class UntagResourceRequestRequestTypeDef(TypedDict):
    ReportName: str
    TagKeys: Sequence[str]

class DeleteReportDefinitionResponseTypeDef(TypedDict):
    ResponseMessage: str
    ResponseMetadata: ResponseMetadataTypeDef

class DescribeReportDefinitionsRequestPaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]

class ListTagsForResourceResponseTypeDef(TypedDict):
    Tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef

class TagResourceRequestRequestTypeDef(TypedDict):
    ReportName: str
    Tags: Sequence[TagTypeDef]

class ReportDefinitionOutputTypeDef(TypedDict):
    ReportName: str
    TimeUnit: TimeUnitType
    Format: ReportFormatType
    Compression: CompressionFormatType
    AdditionalSchemaElements: List[SchemaElementType]
    S3Bucket: str
    S3Prefix: str
    S3Region: AWSRegionType
    AdditionalArtifacts: NotRequired[List[AdditionalArtifactType]]
    RefreshClosedReports: NotRequired[bool]
    ReportVersioning: NotRequired[ReportVersioningType]
    BillingViewArn: NotRequired[str]
    ReportStatus: NotRequired[ReportStatusTypeDef]

class ReportDefinitionTypeDef(TypedDict):
    ReportName: str
    TimeUnit: TimeUnitType
    Format: ReportFormatType
    Compression: CompressionFormatType
    AdditionalSchemaElements: Sequence[SchemaElementType]
    S3Bucket: str
    S3Prefix: str
    S3Region: AWSRegionType
    AdditionalArtifacts: NotRequired[Sequence[AdditionalArtifactType]]
    RefreshClosedReports: NotRequired[bool]
    ReportVersioning: NotRequired[ReportVersioningType]
    BillingViewArn: NotRequired[str]
    ReportStatus: NotRequired[ReportStatusTypeDef]

class DescribeReportDefinitionsResponseTypeDef(TypedDict):
    ReportDefinitions: List[ReportDefinitionOutputTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]

class ModifyReportDefinitionRequestRequestTypeDef(TypedDict):
    ReportName: str
    ReportDefinition: ReportDefinitionTypeDef

class PutReportDefinitionRequestRequestTypeDef(TypedDict):
    ReportDefinition: ReportDefinitionTypeDef
    Tags: NotRequired[Sequence[TagTypeDef]]
