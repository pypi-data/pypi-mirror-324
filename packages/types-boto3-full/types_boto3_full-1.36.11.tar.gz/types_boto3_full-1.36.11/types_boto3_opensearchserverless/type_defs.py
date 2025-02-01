"""
Type annotations for opensearchserverless service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_opensearchserverless/type_defs/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from types_boto3_opensearchserverless.type_defs import AccessPolicyDetailTypeDef

    data: AccessPolicyDetailTypeDef = ...
    ```
"""

from __future__ import annotations

import sys
from typing import Any

from .literals import (
    CollectionStatusType,
    CollectionTypeType,
    IamIdentityCenterGroupAttributeType,
    IamIdentityCenterUserAttributeType,
    SecurityConfigTypeType,
    SecurityPolicyTypeType,
    StandbyReplicasType,
    VpcEndpointStatusType,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import list as List
    from collections.abc import Sequence
else:
    from typing import Dict, List, Sequence
if sys.version_info >= (3, 12):
    from typing import Literal, NotRequired, TypedDict
else:
    from typing_extensions import Literal, NotRequired, TypedDict


__all__ = (
    "AccessPolicyDetailTypeDef",
    "AccessPolicyStatsTypeDef",
    "AccessPolicySummaryTypeDef",
    "AccountSettingsDetailTypeDef",
    "BatchGetCollectionRequestTypeDef",
    "BatchGetCollectionResponseTypeDef",
    "BatchGetEffectiveLifecyclePolicyRequestTypeDef",
    "BatchGetEffectiveLifecyclePolicyResponseTypeDef",
    "BatchGetLifecyclePolicyRequestTypeDef",
    "BatchGetLifecyclePolicyResponseTypeDef",
    "BatchGetVpcEndpointRequestTypeDef",
    "BatchGetVpcEndpointResponseTypeDef",
    "CapacityLimitsTypeDef",
    "CollectionDetailTypeDef",
    "CollectionErrorDetailTypeDef",
    "CollectionFiltersTypeDef",
    "CollectionSummaryTypeDef",
    "CreateAccessPolicyRequestTypeDef",
    "CreateAccessPolicyResponseTypeDef",
    "CreateCollectionDetailTypeDef",
    "CreateCollectionRequestTypeDef",
    "CreateCollectionResponseTypeDef",
    "CreateIamIdentityCenterConfigOptionsTypeDef",
    "CreateLifecyclePolicyRequestTypeDef",
    "CreateLifecyclePolicyResponseTypeDef",
    "CreateSecurityConfigRequestTypeDef",
    "CreateSecurityConfigResponseTypeDef",
    "CreateSecurityPolicyRequestTypeDef",
    "CreateSecurityPolicyResponseTypeDef",
    "CreateVpcEndpointDetailTypeDef",
    "CreateVpcEndpointRequestTypeDef",
    "CreateVpcEndpointResponseTypeDef",
    "DeleteAccessPolicyRequestTypeDef",
    "DeleteCollectionDetailTypeDef",
    "DeleteCollectionRequestTypeDef",
    "DeleteCollectionResponseTypeDef",
    "DeleteLifecyclePolicyRequestTypeDef",
    "DeleteSecurityConfigRequestTypeDef",
    "DeleteSecurityPolicyRequestTypeDef",
    "DeleteVpcEndpointDetailTypeDef",
    "DeleteVpcEndpointRequestTypeDef",
    "DeleteVpcEndpointResponseTypeDef",
    "EffectiveLifecyclePolicyDetailTypeDef",
    "EffectiveLifecyclePolicyErrorDetailTypeDef",
    "GetAccessPolicyRequestTypeDef",
    "GetAccessPolicyResponseTypeDef",
    "GetAccountSettingsResponseTypeDef",
    "GetPoliciesStatsResponseTypeDef",
    "GetSecurityConfigRequestTypeDef",
    "GetSecurityConfigResponseTypeDef",
    "GetSecurityPolicyRequestTypeDef",
    "GetSecurityPolicyResponseTypeDef",
    "IamIdentityCenterConfigOptionsTypeDef",
    "LifecyclePolicyDetailTypeDef",
    "LifecyclePolicyErrorDetailTypeDef",
    "LifecyclePolicyIdentifierTypeDef",
    "LifecyclePolicyResourceIdentifierTypeDef",
    "LifecyclePolicyStatsTypeDef",
    "LifecyclePolicySummaryTypeDef",
    "ListAccessPoliciesRequestTypeDef",
    "ListAccessPoliciesResponseTypeDef",
    "ListCollectionsRequestTypeDef",
    "ListCollectionsResponseTypeDef",
    "ListLifecyclePoliciesRequestTypeDef",
    "ListLifecyclePoliciesResponseTypeDef",
    "ListSecurityConfigsRequestTypeDef",
    "ListSecurityConfigsResponseTypeDef",
    "ListSecurityPoliciesRequestTypeDef",
    "ListSecurityPoliciesResponseTypeDef",
    "ListTagsForResourceRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "ListVpcEndpointsRequestTypeDef",
    "ListVpcEndpointsResponseTypeDef",
    "ResponseMetadataTypeDef",
    "SamlConfigOptionsTypeDef",
    "SecurityConfigDetailTypeDef",
    "SecurityConfigStatsTypeDef",
    "SecurityConfigSummaryTypeDef",
    "SecurityPolicyDetailTypeDef",
    "SecurityPolicyStatsTypeDef",
    "SecurityPolicySummaryTypeDef",
    "TagResourceRequestTypeDef",
    "TagTypeDef",
    "UntagResourceRequestTypeDef",
    "UpdateAccessPolicyRequestTypeDef",
    "UpdateAccessPolicyResponseTypeDef",
    "UpdateAccountSettingsRequestTypeDef",
    "UpdateAccountSettingsResponseTypeDef",
    "UpdateCollectionDetailTypeDef",
    "UpdateCollectionRequestTypeDef",
    "UpdateCollectionResponseTypeDef",
    "UpdateIamIdentityCenterConfigOptionsTypeDef",
    "UpdateLifecyclePolicyRequestTypeDef",
    "UpdateLifecyclePolicyResponseTypeDef",
    "UpdateSecurityConfigRequestTypeDef",
    "UpdateSecurityConfigResponseTypeDef",
    "UpdateSecurityPolicyRequestTypeDef",
    "UpdateSecurityPolicyResponseTypeDef",
    "UpdateVpcEndpointDetailTypeDef",
    "UpdateVpcEndpointRequestTypeDef",
    "UpdateVpcEndpointResponseTypeDef",
    "VpcEndpointDetailTypeDef",
    "VpcEndpointErrorDetailTypeDef",
    "VpcEndpointFiltersTypeDef",
    "VpcEndpointSummaryTypeDef",
)

AccessPolicyDetailTypeDef = TypedDict(
    "AccessPolicyDetailTypeDef",
    {
        "createdDate": NotRequired[int],
        "description": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "name": NotRequired[str],
        "policy": NotRequired[Dict[str, Any]],
        "policyVersion": NotRequired[str],
        "type": NotRequired[Literal["data"]],
    },
)


class AccessPolicyStatsTypeDef(TypedDict):
    DataPolicyCount: NotRequired[int]


AccessPolicySummaryTypeDef = TypedDict(
    "AccessPolicySummaryTypeDef",
    {
        "createdDate": NotRequired[int],
        "description": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "name": NotRequired[str],
        "policyVersion": NotRequired[str],
        "type": NotRequired[Literal["data"]],
    },
)


class CapacityLimitsTypeDef(TypedDict):
    maxIndexingCapacityInOCU: NotRequired[int]
    maxSearchCapacityInOCU: NotRequired[int]


class BatchGetCollectionRequestTypeDef(TypedDict):
    ids: NotRequired[Sequence[str]]
    names: NotRequired[Sequence[str]]


CollectionDetailTypeDef = TypedDict(
    "CollectionDetailTypeDef",
    {
        "arn": NotRequired[str],
        "collectionEndpoint": NotRequired[str],
        "createdDate": NotRequired[int],
        "dashboardEndpoint": NotRequired[str],
        "description": NotRequired[str],
        "failureCode": NotRequired[str],
        "failureMessage": NotRequired[str],
        "id": NotRequired[str],
        "kmsKeyArn": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "name": NotRequired[str],
        "standbyReplicas": NotRequired[StandbyReplicasType],
        "status": NotRequired[CollectionStatusType],
        "type": NotRequired[CollectionTypeType],
    },
)
CollectionErrorDetailTypeDef = TypedDict(
    "CollectionErrorDetailTypeDef",
    {
        "errorCode": NotRequired[str],
        "errorMessage": NotRequired[str],
        "id": NotRequired[str],
        "name": NotRequired[str],
    },
)


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


LifecyclePolicyResourceIdentifierTypeDef = TypedDict(
    "LifecyclePolicyResourceIdentifierTypeDef",
    {
        "resource": str,
        "type": Literal["retention"],
    },
)
EffectiveLifecyclePolicyDetailTypeDef = TypedDict(
    "EffectiveLifecyclePolicyDetailTypeDef",
    {
        "noMinRetentionPeriod": NotRequired[bool],
        "policyName": NotRequired[str],
        "resource": NotRequired[str],
        "resourceType": NotRequired[Literal["index"]],
        "retentionPeriod": NotRequired[str],
        "type": NotRequired[Literal["retention"]],
    },
)
EffectiveLifecyclePolicyErrorDetailTypeDef = TypedDict(
    "EffectiveLifecyclePolicyErrorDetailTypeDef",
    {
        "errorCode": NotRequired[str],
        "errorMessage": NotRequired[str],
        "resource": NotRequired[str],
        "type": NotRequired[Literal["retention"]],
    },
)
LifecyclePolicyIdentifierTypeDef = TypedDict(
    "LifecyclePolicyIdentifierTypeDef",
    {
        "name": str,
        "type": Literal["retention"],
    },
)
LifecyclePolicyDetailTypeDef = TypedDict(
    "LifecyclePolicyDetailTypeDef",
    {
        "createdDate": NotRequired[int],
        "description": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "name": NotRequired[str],
        "policy": NotRequired[Dict[str, Any]],
        "policyVersion": NotRequired[str],
        "type": NotRequired[Literal["retention"]],
    },
)
LifecyclePolicyErrorDetailTypeDef = TypedDict(
    "LifecyclePolicyErrorDetailTypeDef",
    {
        "errorCode": NotRequired[str],
        "errorMessage": NotRequired[str],
        "name": NotRequired[str],
        "type": NotRequired[Literal["retention"]],
    },
)


class BatchGetVpcEndpointRequestTypeDef(TypedDict):
    ids: Sequence[str]


VpcEndpointDetailTypeDef = TypedDict(
    "VpcEndpointDetailTypeDef",
    {
        "createdDate": NotRequired[int],
        "failureCode": NotRequired[str],
        "failureMessage": NotRequired[str],
        "id": NotRequired[str],
        "name": NotRequired[str],
        "securityGroupIds": NotRequired[List[str]],
        "status": NotRequired[VpcEndpointStatusType],
        "subnetIds": NotRequired[List[str]],
        "vpcId": NotRequired[str],
    },
)
VpcEndpointErrorDetailTypeDef = TypedDict(
    "VpcEndpointErrorDetailTypeDef",
    {
        "errorCode": NotRequired[str],
        "errorMessage": NotRequired[str],
        "id": NotRequired[str],
    },
)


class CollectionFiltersTypeDef(TypedDict):
    name: NotRequired[str]
    status: NotRequired[CollectionStatusType]


CollectionSummaryTypeDef = TypedDict(
    "CollectionSummaryTypeDef",
    {
        "arn": NotRequired[str],
        "id": NotRequired[str],
        "name": NotRequired[str],
        "status": NotRequired[CollectionStatusType],
    },
)
CreateAccessPolicyRequestTypeDef = TypedDict(
    "CreateAccessPolicyRequestTypeDef",
    {
        "name": str,
        "policy": str,
        "type": Literal["data"],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
    },
)
CreateCollectionDetailTypeDef = TypedDict(
    "CreateCollectionDetailTypeDef",
    {
        "arn": NotRequired[str],
        "createdDate": NotRequired[int],
        "description": NotRequired[str],
        "id": NotRequired[str],
        "kmsKeyArn": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "name": NotRequired[str],
        "standbyReplicas": NotRequired[StandbyReplicasType],
        "status": NotRequired[CollectionStatusType],
        "type": NotRequired[CollectionTypeType],
    },
)


class TagTypeDef(TypedDict):
    key: str
    value: str


class CreateIamIdentityCenterConfigOptionsTypeDef(TypedDict):
    instanceArn: str
    groupAttribute: NotRequired[IamIdentityCenterGroupAttributeType]
    userAttribute: NotRequired[IamIdentityCenterUserAttributeType]


CreateLifecyclePolicyRequestTypeDef = TypedDict(
    "CreateLifecyclePolicyRequestTypeDef",
    {
        "name": str,
        "policy": str,
        "type": Literal["retention"],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
    },
)


class SamlConfigOptionsTypeDef(TypedDict):
    metadata: str
    groupAttribute: NotRequired[str]
    sessionTimeout: NotRequired[int]
    userAttribute: NotRequired[str]


CreateSecurityPolicyRequestTypeDef = TypedDict(
    "CreateSecurityPolicyRequestTypeDef",
    {
        "name": str,
        "policy": str,
        "type": SecurityPolicyTypeType,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
    },
)
SecurityPolicyDetailTypeDef = TypedDict(
    "SecurityPolicyDetailTypeDef",
    {
        "createdDate": NotRequired[int],
        "description": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "name": NotRequired[str],
        "policy": NotRequired[Dict[str, Any]],
        "policyVersion": NotRequired[str],
        "type": NotRequired[SecurityPolicyTypeType],
    },
)
CreateVpcEndpointDetailTypeDef = TypedDict(
    "CreateVpcEndpointDetailTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "status": NotRequired[VpcEndpointStatusType],
    },
)


class CreateVpcEndpointRequestTypeDef(TypedDict):
    name: str
    subnetIds: Sequence[str]
    vpcId: str
    clientToken: NotRequired[str]
    securityGroupIds: NotRequired[Sequence[str]]


DeleteAccessPolicyRequestTypeDef = TypedDict(
    "DeleteAccessPolicyRequestTypeDef",
    {
        "name": str,
        "type": Literal["data"],
        "clientToken": NotRequired[str],
    },
)
DeleteCollectionDetailTypeDef = TypedDict(
    "DeleteCollectionDetailTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "status": NotRequired[CollectionStatusType],
    },
)
DeleteCollectionRequestTypeDef = TypedDict(
    "DeleteCollectionRequestTypeDef",
    {
        "id": str,
        "clientToken": NotRequired[str],
    },
)
DeleteLifecyclePolicyRequestTypeDef = TypedDict(
    "DeleteLifecyclePolicyRequestTypeDef",
    {
        "name": str,
        "type": Literal["retention"],
        "clientToken": NotRequired[str],
    },
)
DeleteSecurityConfigRequestTypeDef = TypedDict(
    "DeleteSecurityConfigRequestTypeDef",
    {
        "id": str,
        "clientToken": NotRequired[str],
    },
)
DeleteSecurityPolicyRequestTypeDef = TypedDict(
    "DeleteSecurityPolicyRequestTypeDef",
    {
        "name": str,
        "type": SecurityPolicyTypeType,
        "clientToken": NotRequired[str],
    },
)
DeleteVpcEndpointDetailTypeDef = TypedDict(
    "DeleteVpcEndpointDetailTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "status": NotRequired[VpcEndpointStatusType],
    },
)
DeleteVpcEndpointRequestTypeDef = TypedDict(
    "DeleteVpcEndpointRequestTypeDef",
    {
        "id": str,
        "clientToken": NotRequired[str],
    },
)
GetAccessPolicyRequestTypeDef = TypedDict(
    "GetAccessPolicyRequestTypeDef",
    {
        "name": str,
        "type": Literal["data"],
    },
)


class LifecyclePolicyStatsTypeDef(TypedDict):
    RetentionPolicyCount: NotRequired[int]


class SecurityConfigStatsTypeDef(TypedDict):
    SamlConfigCount: NotRequired[int]


class SecurityPolicyStatsTypeDef(TypedDict):
    EncryptionPolicyCount: NotRequired[int]
    NetworkPolicyCount: NotRequired[int]


GetSecurityConfigRequestTypeDef = TypedDict(
    "GetSecurityConfigRequestTypeDef",
    {
        "id": str,
    },
)
GetSecurityPolicyRequestTypeDef = TypedDict(
    "GetSecurityPolicyRequestTypeDef",
    {
        "name": str,
        "type": SecurityPolicyTypeType,
    },
)


class IamIdentityCenterConfigOptionsTypeDef(TypedDict):
    applicationArn: NotRequired[str]
    applicationDescription: NotRequired[str]
    applicationName: NotRequired[str]
    groupAttribute: NotRequired[IamIdentityCenterGroupAttributeType]
    instanceArn: NotRequired[str]
    userAttribute: NotRequired[IamIdentityCenterUserAttributeType]


LifecyclePolicySummaryTypeDef = TypedDict(
    "LifecyclePolicySummaryTypeDef",
    {
        "createdDate": NotRequired[int],
        "description": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "name": NotRequired[str],
        "policyVersion": NotRequired[str],
        "type": NotRequired[Literal["retention"]],
    },
)
ListAccessPoliciesRequestTypeDef = TypedDict(
    "ListAccessPoliciesRequestTypeDef",
    {
        "type": Literal["data"],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "resource": NotRequired[Sequence[str]],
    },
)
ListLifecyclePoliciesRequestTypeDef = TypedDict(
    "ListLifecyclePoliciesRequestTypeDef",
    {
        "type": Literal["retention"],
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "resources": NotRequired[Sequence[str]],
    },
)
ListSecurityConfigsRequestTypeDef = TypedDict(
    "ListSecurityConfigsRequestTypeDef",
    {
        "type": SecurityConfigTypeType,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
    },
)
SecurityConfigSummaryTypeDef = TypedDict(
    "SecurityConfigSummaryTypeDef",
    {
        "configVersion": NotRequired[str],
        "createdDate": NotRequired[int],
        "description": NotRequired[str],
        "id": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "type": NotRequired[SecurityConfigTypeType],
    },
)
ListSecurityPoliciesRequestTypeDef = TypedDict(
    "ListSecurityPoliciesRequestTypeDef",
    {
        "type": SecurityPolicyTypeType,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "resource": NotRequired[Sequence[str]],
    },
)
SecurityPolicySummaryTypeDef = TypedDict(
    "SecurityPolicySummaryTypeDef",
    {
        "createdDate": NotRequired[int],
        "description": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "name": NotRequired[str],
        "policyVersion": NotRequired[str],
        "type": NotRequired[SecurityPolicyTypeType],
    },
)


class ListTagsForResourceRequestTypeDef(TypedDict):
    resourceArn: str


class VpcEndpointFiltersTypeDef(TypedDict):
    status: NotRequired[VpcEndpointStatusType]


VpcEndpointSummaryTypeDef = TypedDict(
    "VpcEndpointSummaryTypeDef",
    {
        "id": NotRequired[str],
        "name": NotRequired[str],
        "status": NotRequired[VpcEndpointStatusType],
    },
)


class UntagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


UpdateAccessPolicyRequestTypeDef = TypedDict(
    "UpdateAccessPolicyRequestTypeDef",
    {
        "name": str,
        "policyVersion": str,
        "type": Literal["data"],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "policy": NotRequired[str],
    },
)
UpdateCollectionDetailTypeDef = TypedDict(
    "UpdateCollectionDetailTypeDef",
    {
        "arn": NotRequired[str],
        "createdDate": NotRequired[int],
        "description": NotRequired[str],
        "id": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "name": NotRequired[str],
        "status": NotRequired[CollectionStatusType],
        "type": NotRequired[CollectionTypeType],
    },
)
UpdateCollectionRequestTypeDef = TypedDict(
    "UpdateCollectionRequestTypeDef",
    {
        "id": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
    },
)


class UpdateIamIdentityCenterConfigOptionsTypeDef(TypedDict):
    groupAttribute: NotRequired[IamIdentityCenterGroupAttributeType]
    userAttribute: NotRequired[IamIdentityCenterUserAttributeType]


UpdateLifecyclePolicyRequestTypeDef = TypedDict(
    "UpdateLifecyclePolicyRequestTypeDef",
    {
        "name": str,
        "policyVersion": str,
        "type": Literal["retention"],
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "policy": NotRequired[str],
    },
)
UpdateSecurityPolicyRequestTypeDef = TypedDict(
    "UpdateSecurityPolicyRequestTypeDef",
    {
        "name": str,
        "policyVersion": str,
        "type": SecurityPolicyTypeType,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "policy": NotRequired[str],
    },
)
UpdateVpcEndpointDetailTypeDef = TypedDict(
    "UpdateVpcEndpointDetailTypeDef",
    {
        "id": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "name": NotRequired[str],
        "securityGroupIds": NotRequired[List[str]],
        "status": NotRequired[VpcEndpointStatusType],
        "subnetIds": NotRequired[List[str]],
    },
)
UpdateVpcEndpointRequestTypeDef = TypedDict(
    "UpdateVpcEndpointRequestTypeDef",
    {
        "id": str,
        "addSecurityGroupIds": NotRequired[Sequence[str]],
        "addSubnetIds": NotRequired[Sequence[str]],
        "clientToken": NotRequired[str],
        "removeSecurityGroupIds": NotRequired[Sequence[str]],
        "removeSubnetIds": NotRequired[Sequence[str]],
    },
)


class AccountSettingsDetailTypeDef(TypedDict):
    capacityLimits: NotRequired[CapacityLimitsTypeDef]


class UpdateAccountSettingsRequestTypeDef(TypedDict):
    capacityLimits: NotRequired[CapacityLimitsTypeDef]


class BatchGetCollectionResponseTypeDef(TypedDict):
    collectionDetails: List[CollectionDetailTypeDef]
    collectionErrorDetails: List[CollectionErrorDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateAccessPolicyResponseTypeDef(TypedDict):
    accessPolicyDetail: AccessPolicyDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAccessPolicyResponseTypeDef(TypedDict):
    accessPolicyDetail: AccessPolicyDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ListAccessPoliciesResponseTypeDef(TypedDict):
    accessPolicySummaries: List[AccessPolicySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateAccessPolicyResponseTypeDef(TypedDict):
    accessPolicyDetail: AccessPolicyDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class BatchGetEffectiveLifecyclePolicyRequestTypeDef(TypedDict):
    resourceIdentifiers: Sequence[LifecyclePolicyResourceIdentifierTypeDef]


class BatchGetEffectiveLifecyclePolicyResponseTypeDef(TypedDict):
    effectiveLifecyclePolicyDetails: List[EffectiveLifecyclePolicyDetailTypeDef]
    effectiveLifecyclePolicyErrorDetails: List[EffectiveLifecyclePolicyErrorDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchGetLifecyclePolicyRequestTypeDef(TypedDict):
    identifiers: Sequence[LifecyclePolicyIdentifierTypeDef]


class CreateLifecyclePolicyResponseTypeDef(TypedDict):
    lifecyclePolicyDetail: LifecyclePolicyDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateLifecyclePolicyResponseTypeDef(TypedDict):
    lifecyclePolicyDetail: LifecyclePolicyDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class BatchGetLifecyclePolicyResponseTypeDef(TypedDict):
    lifecyclePolicyDetails: List[LifecyclePolicyDetailTypeDef]
    lifecyclePolicyErrorDetails: List[LifecyclePolicyErrorDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class BatchGetVpcEndpointResponseTypeDef(TypedDict):
    vpcEndpointDetails: List[VpcEndpointDetailTypeDef]
    vpcEndpointErrorDetails: List[VpcEndpointErrorDetailTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ListCollectionsRequestTypeDef(TypedDict):
    collectionFilters: NotRequired[CollectionFiltersTypeDef]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListCollectionsResponseTypeDef(TypedDict):
    collectionSummaries: List[CollectionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class CreateCollectionResponseTypeDef(TypedDict):
    createCollectionDetail: CreateCollectionDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


CreateCollectionRequestTypeDef = TypedDict(
    "CreateCollectionRequestTypeDef",
    {
        "name": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "standbyReplicas": NotRequired[StandbyReplicasType],
        "tags": NotRequired[Sequence[TagTypeDef]],
        "type": NotRequired[CollectionTypeType],
    },
)


class ListTagsForResourceResponseTypeDef(TypedDict):
    tags: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TagResourceRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Sequence[TagTypeDef]


CreateSecurityConfigRequestTypeDef = TypedDict(
    "CreateSecurityConfigRequestTypeDef",
    {
        "name": str,
        "type": SecurityConfigTypeType,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "iamIdentityCenterOptions": NotRequired[CreateIamIdentityCenterConfigOptionsTypeDef],
        "samlOptions": NotRequired[SamlConfigOptionsTypeDef],
    },
)


class CreateSecurityPolicyResponseTypeDef(TypedDict):
    securityPolicyDetail: SecurityPolicyDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetSecurityPolicyResponseTypeDef(TypedDict):
    securityPolicyDetail: SecurityPolicyDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSecurityPolicyResponseTypeDef(TypedDict):
    securityPolicyDetail: SecurityPolicyDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateVpcEndpointResponseTypeDef(TypedDict):
    createVpcEndpointDetail: CreateVpcEndpointDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteCollectionResponseTypeDef(TypedDict):
    deleteCollectionDetail: DeleteCollectionDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteVpcEndpointResponseTypeDef(TypedDict):
    deleteVpcEndpointDetail: DeleteVpcEndpointDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetPoliciesStatsResponseTypeDef(TypedDict):
    AccessPolicyStats: AccessPolicyStatsTypeDef
    LifecyclePolicyStats: LifecyclePolicyStatsTypeDef
    SecurityConfigStats: SecurityConfigStatsTypeDef
    SecurityPolicyStats: SecurityPolicyStatsTypeDef
    TotalPolicyCount: int
    ResponseMetadata: ResponseMetadataTypeDef


SecurityConfigDetailTypeDef = TypedDict(
    "SecurityConfigDetailTypeDef",
    {
        "configVersion": NotRequired[str],
        "createdDate": NotRequired[int],
        "description": NotRequired[str],
        "iamIdentityCenterOptions": NotRequired[IamIdentityCenterConfigOptionsTypeDef],
        "id": NotRequired[str],
        "lastModifiedDate": NotRequired[int],
        "samlOptions": NotRequired[SamlConfigOptionsTypeDef],
        "type": NotRequired[SecurityConfigTypeType],
    },
)


class ListLifecyclePoliciesResponseTypeDef(TypedDict):
    lifecyclePolicySummaries: List[LifecyclePolicySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSecurityConfigsResponseTypeDef(TypedDict):
    securityConfigSummaries: List[SecurityConfigSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListSecurityPoliciesResponseTypeDef(TypedDict):
    securityPolicySummaries: List[SecurityPolicySummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListVpcEndpointsRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    vpcEndpointFilters: NotRequired[VpcEndpointFiltersTypeDef]


class ListVpcEndpointsResponseTypeDef(TypedDict):
    vpcEndpointSummaries: List[VpcEndpointSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class UpdateCollectionResponseTypeDef(TypedDict):
    updateCollectionDetail: UpdateCollectionDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


UpdateSecurityConfigRequestTypeDef = TypedDict(
    "UpdateSecurityConfigRequestTypeDef",
    {
        "configVersion": str,
        "id": str,
        "clientToken": NotRequired[str],
        "description": NotRequired[str],
        "iamIdentityCenterOptionsUpdates": NotRequired[UpdateIamIdentityCenterConfigOptionsTypeDef],
        "samlOptions": NotRequired[SamlConfigOptionsTypeDef],
    },
)


class UpdateVpcEndpointResponseTypeDef(TypedDict):
    UpdateVpcEndpointDetail: UpdateVpcEndpointDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetAccountSettingsResponseTypeDef(TypedDict):
    accountSettingsDetail: AccountSettingsDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateAccountSettingsResponseTypeDef(TypedDict):
    accountSettingsDetail: AccountSettingsDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateSecurityConfigResponseTypeDef(TypedDict):
    securityConfigDetail: SecurityConfigDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class GetSecurityConfigResponseTypeDef(TypedDict):
    securityConfigDetail: SecurityConfigDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSecurityConfigResponseTypeDef(TypedDict):
    securityConfigDetail: SecurityConfigDetailTypeDef
    ResponseMetadata: ResponseMetadataTypeDef
