"""
Type annotations for snow-device-management service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_snow_device_management/type_defs/)

Usage::

    ```python
    from types_boto3_snow_device_management.type_defs import CancelTaskInputRequestTypeDef

    data: CancelTaskInputRequestTypeDef = ...
    ```

Copyright 2025 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import Any

from .literals import (
    AttachmentStatusType,
    ExecutionStateType,
    InstanceStateNameType,
    IpAddressAssignmentType,
    PhysicalConnectorTypeType,
    TaskStateType,
    UnlockStateType,
)

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
    "CancelTaskInputRequestTypeDef",
    "CancelTaskOutputTypeDef",
    "CapacityTypeDef",
    "CommandTypeDef",
    "CpuOptionsTypeDef",
    "CreateTaskInputRequestTypeDef",
    "CreateTaskOutputTypeDef",
    "DescribeDeviceEc2InputRequestTypeDef",
    "DescribeDeviceEc2OutputTypeDef",
    "DescribeDeviceInputRequestTypeDef",
    "DescribeDeviceOutputTypeDef",
    "DescribeExecutionInputRequestTypeDef",
    "DescribeExecutionOutputTypeDef",
    "DescribeTaskInputRequestTypeDef",
    "DescribeTaskOutputTypeDef",
    "DeviceSummaryTypeDef",
    "EbsInstanceBlockDeviceTypeDef",
    "EmptyResponseMetadataTypeDef",
    "ExecutionSummaryTypeDef",
    "InstanceBlockDeviceMappingTypeDef",
    "InstanceStateTypeDef",
    "InstanceSummaryTypeDef",
    "InstanceTypeDef",
    "ListDeviceResourcesInputPaginateTypeDef",
    "ListDeviceResourcesInputRequestTypeDef",
    "ListDeviceResourcesOutputTypeDef",
    "ListDevicesInputPaginateTypeDef",
    "ListDevicesInputRequestTypeDef",
    "ListDevicesOutputTypeDef",
    "ListExecutionsInputPaginateTypeDef",
    "ListExecutionsInputRequestTypeDef",
    "ListExecutionsOutputTypeDef",
    "ListTagsForResourceInputRequestTypeDef",
    "ListTagsForResourceOutputTypeDef",
    "ListTasksInputPaginateTypeDef",
    "ListTasksInputRequestTypeDef",
    "ListTasksOutputTypeDef",
    "PaginatorConfigTypeDef",
    "PhysicalNetworkInterfaceTypeDef",
    "ResourceSummaryTypeDef",
    "ResponseMetadataTypeDef",
    "SecurityGroupIdentifierTypeDef",
    "SoftwareInformationTypeDef",
    "TagResourceInputRequestTypeDef",
    "TaskSummaryTypeDef",
    "UntagResourceInputRequestTypeDef",
)


class CancelTaskInputRequestTypeDef(TypedDict):
    taskId: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class CapacityTypeDef(TypedDict):
    available: NotRequired[int]
    name: NotRequired[str]
    total: NotRequired[int]
    unit: NotRequired[str]
    used: NotRequired[int]


class CommandTypeDef(TypedDict):
    reboot: NotRequired[Mapping[str, Any]]
    unlock: NotRequired[Mapping[str, Any]]


class CpuOptionsTypeDef(TypedDict):
    coreCount: NotRequired[int]
    threadsPerCore: NotRequired[int]


class DescribeDeviceEc2InputRequestTypeDef(TypedDict):
    instanceIds: Sequence[str]
    managedDeviceId: str


class DescribeDeviceInputRequestTypeDef(TypedDict):
    managedDeviceId: str


class PhysicalNetworkInterfaceTypeDef(TypedDict):
    defaultGateway: NotRequired[str]
    ipAddress: NotRequired[str]
    ipAddressAssignment: NotRequired[IpAddressAssignmentType]
    macAddress: NotRequired[str]
    netmask: NotRequired[str]
    physicalConnectorType: NotRequired[PhysicalConnectorTypeType]
    physicalNetworkInterfaceId: NotRequired[str]


class SoftwareInformationTypeDef(TypedDict):
    installState: NotRequired[str]
    installedVersion: NotRequired[str]
    installingVersion: NotRequired[str]


class DescribeExecutionInputRequestTypeDef(TypedDict):
    managedDeviceId: str
    taskId: str


class DescribeTaskInputRequestTypeDef(TypedDict):
    taskId: str


class DeviceSummaryTypeDef(TypedDict):
    associatedWithJob: NotRequired[str]
    managedDeviceArn: NotRequired[str]
    managedDeviceId: NotRequired[str]
    tags: NotRequired[Dict[str, str]]


class EbsInstanceBlockDeviceTypeDef(TypedDict):
    attachTime: NotRequired[datetime]
    deleteOnTermination: NotRequired[bool]
    status: NotRequired[AttachmentStatusType]
    volumeId: NotRequired[str]


class ExecutionSummaryTypeDef(TypedDict):
    executionId: NotRequired[str]
    managedDeviceId: NotRequired[str]
    state: NotRequired[ExecutionStateType]
    taskId: NotRequired[str]


class InstanceStateTypeDef(TypedDict):
    code: NotRequired[int]
    name: NotRequired[InstanceStateNameType]


class SecurityGroupIdentifierTypeDef(TypedDict):
    groupId: NotRequired[str]
    groupName: NotRequired[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


ListDeviceResourcesInputRequestTypeDef = TypedDict(
    "ListDeviceResourcesInputRequestTypeDef",
    {
        "managedDeviceId": str,
        "maxResults": NotRequired[int],
        "nextToken": NotRequired[str],
        "type": NotRequired[str],
    },
)
ResourceSummaryTypeDef = TypedDict(
    "ResourceSummaryTypeDef",
    {
        "resourceType": str,
        "arn": NotRequired[str],
        "id": NotRequired[str],
    },
)


class ListDevicesInputRequestTypeDef(TypedDict):
    jobId: NotRequired[str]
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]


class ListExecutionsInputRequestTypeDef(TypedDict):
    taskId: str
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    state: NotRequired[ExecutionStateType]


class ListTagsForResourceInputRequestTypeDef(TypedDict):
    resourceArn: str


class ListTasksInputRequestTypeDef(TypedDict):
    maxResults: NotRequired[int]
    nextToken: NotRequired[str]
    state: NotRequired[TaskStateType]


class TaskSummaryTypeDef(TypedDict):
    taskId: str
    state: NotRequired[TaskStateType]
    tags: NotRequired[Dict[str, str]]
    taskArn: NotRequired[str]


class TagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tags: Mapping[str, str]


class UntagResourceInputRequestTypeDef(TypedDict):
    resourceArn: str
    tagKeys: Sequence[str]


class CancelTaskOutputTypeDef(TypedDict):
    taskId: str
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTaskOutputTypeDef(TypedDict):
    taskArn: str
    taskId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeExecutionOutputTypeDef(TypedDict):
    executionId: str
    lastUpdatedAt: datetime
    managedDeviceId: str
    startedAt: datetime
    state: ExecutionStateType
    taskId: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTaskOutputTypeDef(TypedDict):
    completedAt: datetime
    createdAt: datetime
    description: str
    lastUpdatedAt: datetime
    state: TaskStateType
    tags: Dict[str, str]
    targets: List[str]
    taskArn: str
    taskId: str
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceOutputTypeDef(TypedDict):
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class CreateTaskInputRequestTypeDef(TypedDict):
    command: CommandTypeDef
    targets: Sequence[str]
    clientToken: NotRequired[str]
    description: NotRequired[str]
    tags: NotRequired[Mapping[str, str]]


class DescribeDeviceOutputTypeDef(TypedDict):
    associatedWithJob: str
    deviceCapacities: List[CapacityTypeDef]
    deviceState: UnlockStateType
    deviceType: str
    lastReachedOutAt: datetime
    lastUpdatedAt: datetime
    managedDeviceArn: str
    managedDeviceId: str
    physicalNetworkInterfaces: List[PhysicalNetworkInterfaceTypeDef]
    software: SoftwareInformationTypeDef
    tags: Dict[str, str]
    ResponseMetadata: ResponseMetadataTypeDef


class ListDevicesOutputTypeDef(TypedDict):
    devices: List[DeviceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class InstanceBlockDeviceMappingTypeDef(TypedDict):
    deviceName: NotRequired[str]
    ebs: NotRequired[EbsInstanceBlockDeviceTypeDef]


class ListExecutionsOutputTypeDef(TypedDict):
    executions: List[ExecutionSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


ListDeviceResourcesInputPaginateTypeDef = TypedDict(
    "ListDeviceResourcesInputPaginateTypeDef",
    {
        "managedDeviceId": str,
        "type": NotRequired[str],
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)


class ListDevicesInputPaginateTypeDef(TypedDict):
    jobId: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListExecutionsInputPaginateTypeDef(TypedDict):
    taskId: str
    state: NotRequired[ExecutionStateType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListTasksInputPaginateTypeDef(TypedDict):
    state: NotRequired[TaskStateType]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class ListDeviceResourcesOutputTypeDef(TypedDict):
    resources: List[ResourceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class ListTasksOutputTypeDef(TypedDict):
    tasks: List[TaskSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    nextToken: NotRequired[str]


class InstanceTypeDef(TypedDict):
    amiLaunchIndex: NotRequired[int]
    blockDeviceMappings: NotRequired[List[InstanceBlockDeviceMappingTypeDef]]
    cpuOptions: NotRequired[CpuOptionsTypeDef]
    createdAt: NotRequired[datetime]
    imageId: NotRequired[str]
    instanceId: NotRequired[str]
    instanceType: NotRequired[str]
    privateIpAddress: NotRequired[str]
    publicIpAddress: NotRequired[str]
    rootDeviceName: NotRequired[str]
    securityGroups: NotRequired[List[SecurityGroupIdentifierTypeDef]]
    state: NotRequired[InstanceStateTypeDef]
    updatedAt: NotRequired[datetime]


class InstanceSummaryTypeDef(TypedDict):
    instance: NotRequired[InstanceTypeDef]
    lastUpdatedAt: NotRequired[datetime]


class DescribeDeviceEc2OutputTypeDef(TypedDict):
    instances: List[InstanceSummaryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
