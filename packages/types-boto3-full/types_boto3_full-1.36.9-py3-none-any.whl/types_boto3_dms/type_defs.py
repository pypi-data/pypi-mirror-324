"""
Type annotations for dms service type definitions.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_dms/type_defs/)

Usage::

    ```python
    from types_boto3_dms.type_defs import AccountQuotaTypeDef

    data: AccountQuotaTypeDef = ...
    ```

Copyright 2025 Vlad Emelianov
"""

from __future__ import annotations

import sys
from datetime import datetime
from typing import IO, Any, Union

from botocore.response import StreamingBody

from .literals import (
    AssessmentReportTypeType,
    AuthMechanismValueType,
    AuthTypeValueType,
    CannedAclForObjectsValueType,
    CharLengthSemanticsType,
    CollectorStatusType,
    CompressionTypeValueType,
    DatabaseModeType,
    DataFormatValueType,
    DatePartitionDelimiterValueType,
    DatePartitionSequenceValueType,
    DmsSslModeValueType,
    EncodingTypeValueType,
    EncryptionModeValueType,
    EndpointSettingTypeValueType,
    KafkaSaslMechanismType,
    KafkaSecurityProtocolType,
    KafkaSslEndpointIdentificationAlgorithmType,
    LongVarcharMappingTypeType,
    MessageFormatValueType,
    MigrationTypeValueType,
    NestingLevelValueType,
    OracleAuthenticationMethodType,
    OriginTypeValueType,
    ParquetVersionValueType,
    PluginNameValueType,
    RedisAuthTypeValueType,
    RefreshSchemasStatusTypeValueType,
    ReleaseStatusValuesType,
    ReloadOptionValueType,
    ReplicationEndpointTypeValueType,
    SafeguardPolicyType,
    SqlServerAuthenticationMethodType,
    SslSecurityProtocolValueType,
    StartReplicationMigrationTypeValueType,
    StartReplicationTaskTypeValueType,
    TargetDbTypeType,
    TlogAccessModeType,
    VersionStatusType,
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
    "AccountQuotaTypeDef",
    "AddTagsToResourceMessageRequestTypeDef",
    "ApplyPendingMaintenanceActionMessageRequestTypeDef",
    "ApplyPendingMaintenanceActionResponseTypeDef",
    "AvailabilityZoneTypeDef",
    "BatchStartRecommendationsErrorEntryTypeDef",
    "BatchStartRecommendationsRequestRequestTypeDef",
    "BatchStartRecommendationsResponseTypeDef",
    "BlobTypeDef",
    "CancelReplicationTaskAssessmentRunMessageRequestTypeDef",
    "CancelReplicationTaskAssessmentRunResponseTypeDef",
    "CertificateTypeDef",
    "CollectorHealthCheckTypeDef",
    "CollectorResponseTypeDef",
    "CollectorShortInfoResponseTypeDef",
    "ComputeConfigOutputTypeDef",
    "ComputeConfigTypeDef",
    "ConnectionTypeDef",
    "CreateDataMigrationMessageRequestTypeDef",
    "CreateDataMigrationResponseTypeDef",
    "CreateDataProviderMessageRequestTypeDef",
    "CreateDataProviderResponseTypeDef",
    "CreateEndpointMessageRequestTypeDef",
    "CreateEndpointResponseTypeDef",
    "CreateEventSubscriptionMessageRequestTypeDef",
    "CreateEventSubscriptionResponseTypeDef",
    "CreateFleetAdvisorCollectorRequestRequestTypeDef",
    "CreateFleetAdvisorCollectorResponseTypeDef",
    "CreateInstanceProfileMessageRequestTypeDef",
    "CreateInstanceProfileResponseTypeDef",
    "CreateMigrationProjectMessageRequestTypeDef",
    "CreateMigrationProjectResponseTypeDef",
    "CreateReplicationConfigMessageRequestTypeDef",
    "CreateReplicationConfigResponseTypeDef",
    "CreateReplicationInstanceMessageRequestTypeDef",
    "CreateReplicationInstanceResponseTypeDef",
    "CreateReplicationSubnetGroupMessageRequestTypeDef",
    "CreateReplicationSubnetGroupResponseTypeDef",
    "CreateReplicationTaskMessageRequestTypeDef",
    "CreateReplicationTaskResponseTypeDef",
    "DataMigrationSettingsTypeDef",
    "DataMigrationStatisticsTypeDef",
    "DataMigrationTypeDef",
    "DataProviderDescriptorDefinitionTypeDef",
    "DataProviderDescriptorTypeDef",
    "DataProviderSettingsTypeDef",
    "DataProviderTypeDef",
    "DatabaseInstanceSoftwareDetailsResponseTypeDef",
    "DatabaseResponseTypeDef",
    "DatabaseShortInfoResponseTypeDef",
    "DefaultErrorDetailsTypeDef",
    "DeleteCertificateMessageRequestTypeDef",
    "DeleteCertificateResponseTypeDef",
    "DeleteCollectorRequestRequestTypeDef",
    "DeleteConnectionMessageRequestTypeDef",
    "DeleteConnectionResponseTypeDef",
    "DeleteDataMigrationMessageRequestTypeDef",
    "DeleteDataMigrationResponseTypeDef",
    "DeleteDataProviderMessageRequestTypeDef",
    "DeleteDataProviderResponseTypeDef",
    "DeleteEndpointMessageRequestTypeDef",
    "DeleteEndpointResponseTypeDef",
    "DeleteEventSubscriptionMessageRequestTypeDef",
    "DeleteEventSubscriptionResponseTypeDef",
    "DeleteFleetAdvisorDatabasesRequestRequestTypeDef",
    "DeleteFleetAdvisorDatabasesResponseTypeDef",
    "DeleteInstanceProfileMessageRequestTypeDef",
    "DeleteInstanceProfileResponseTypeDef",
    "DeleteMigrationProjectMessageRequestTypeDef",
    "DeleteMigrationProjectResponseTypeDef",
    "DeleteReplicationConfigMessageRequestTypeDef",
    "DeleteReplicationConfigResponseTypeDef",
    "DeleteReplicationInstanceMessageRequestTypeDef",
    "DeleteReplicationInstanceResponseTypeDef",
    "DeleteReplicationSubnetGroupMessageRequestTypeDef",
    "DeleteReplicationTaskAssessmentRunMessageRequestTypeDef",
    "DeleteReplicationTaskAssessmentRunResponseTypeDef",
    "DeleteReplicationTaskMessageRequestTypeDef",
    "DeleteReplicationTaskResponseTypeDef",
    "DescribeAccountAttributesResponseTypeDef",
    "DescribeApplicableIndividualAssessmentsMessageRequestTypeDef",
    "DescribeApplicableIndividualAssessmentsResponseTypeDef",
    "DescribeCertificatesMessagePaginateTypeDef",
    "DescribeCertificatesMessageRequestTypeDef",
    "DescribeCertificatesResponseTypeDef",
    "DescribeConnectionsMessagePaginateTypeDef",
    "DescribeConnectionsMessageRequestTypeDef",
    "DescribeConnectionsMessageWaitTypeDef",
    "DescribeConnectionsResponseTypeDef",
    "DescribeConversionConfigurationMessageRequestTypeDef",
    "DescribeConversionConfigurationResponseTypeDef",
    "DescribeDataMigrationsMessagePaginateTypeDef",
    "DescribeDataMigrationsMessageRequestTypeDef",
    "DescribeDataMigrationsResponseTypeDef",
    "DescribeDataProvidersMessageRequestTypeDef",
    "DescribeDataProvidersResponseTypeDef",
    "DescribeEndpointSettingsMessageRequestTypeDef",
    "DescribeEndpointSettingsResponseTypeDef",
    "DescribeEndpointTypesMessagePaginateTypeDef",
    "DescribeEndpointTypesMessageRequestTypeDef",
    "DescribeEndpointTypesResponseTypeDef",
    "DescribeEndpointsMessagePaginateTypeDef",
    "DescribeEndpointsMessageRequestTypeDef",
    "DescribeEndpointsMessageWaitTypeDef",
    "DescribeEndpointsResponseTypeDef",
    "DescribeEngineVersionsMessageRequestTypeDef",
    "DescribeEngineVersionsResponseTypeDef",
    "DescribeEventCategoriesMessageRequestTypeDef",
    "DescribeEventCategoriesResponseTypeDef",
    "DescribeEventSubscriptionsMessagePaginateTypeDef",
    "DescribeEventSubscriptionsMessageRequestTypeDef",
    "DescribeEventSubscriptionsResponseTypeDef",
    "DescribeEventsMessagePaginateTypeDef",
    "DescribeEventsMessageRequestTypeDef",
    "DescribeEventsResponseTypeDef",
    "DescribeExtensionPackAssociationsMessageRequestTypeDef",
    "DescribeExtensionPackAssociationsResponseTypeDef",
    "DescribeFleetAdvisorCollectorsRequestRequestTypeDef",
    "DescribeFleetAdvisorCollectorsResponseTypeDef",
    "DescribeFleetAdvisorDatabasesRequestRequestTypeDef",
    "DescribeFleetAdvisorDatabasesResponseTypeDef",
    "DescribeFleetAdvisorLsaAnalysisRequestRequestTypeDef",
    "DescribeFleetAdvisorLsaAnalysisResponseTypeDef",
    "DescribeFleetAdvisorSchemaObjectSummaryRequestRequestTypeDef",
    "DescribeFleetAdvisorSchemaObjectSummaryResponseTypeDef",
    "DescribeFleetAdvisorSchemasRequestRequestTypeDef",
    "DescribeFleetAdvisorSchemasResponseTypeDef",
    "DescribeInstanceProfilesMessageRequestTypeDef",
    "DescribeInstanceProfilesResponseTypeDef",
    "DescribeMetadataModelAssessmentsMessageRequestTypeDef",
    "DescribeMetadataModelAssessmentsResponseTypeDef",
    "DescribeMetadataModelConversionsMessageRequestTypeDef",
    "DescribeMetadataModelConversionsResponseTypeDef",
    "DescribeMetadataModelExportsAsScriptMessageRequestTypeDef",
    "DescribeMetadataModelExportsAsScriptResponseTypeDef",
    "DescribeMetadataModelExportsToTargetMessageRequestTypeDef",
    "DescribeMetadataModelExportsToTargetResponseTypeDef",
    "DescribeMetadataModelImportsMessageRequestTypeDef",
    "DescribeMetadataModelImportsResponseTypeDef",
    "DescribeMigrationProjectsMessageRequestTypeDef",
    "DescribeMigrationProjectsResponseTypeDef",
    "DescribeOrderableReplicationInstancesMessagePaginateTypeDef",
    "DescribeOrderableReplicationInstancesMessageRequestTypeDef",
    "DescribeOrderableReplicationInstancesResponseTypeDef",
    "DescribePendingMaintenanceActionsMessageRequestTypeDef",
    "DescribePendingMaintenanceActionsResponseTypeDef",
    "DescribeRecommendationLimitationsRequestRequestTypeDef",
    "DescribeRecommendationLimitationsResponseTypeDef",
    "DescribeRecommendationsRequestRequestTypeDef",
    "DescribeRecommendationsResponseTypeDef",
    "DescribeRefreshSchemasStatusMessageRequestTypeDef",
    "DescribeRefreshSchemasStatusResponseTypeDef",
    "DescribeReplicationConfigsMessageRequestTypeDef",
    "DescribeReplicationConfigsResponseTypeDef",
    "DescribeReplicationInstanceTaskLogsMessageRequestTypeDef",
    "DescribeReplicationInstanceTaskLogsResponseTypeDef",
    "DescribeReplicationInstancesMessagePaginateTypeDef",
    "DescribeReplicationInstancesMessageRequestTypeDef",
    "DescribeReplicationInstancesMessageWaitTypeDef",
    "DescribeReplicationInstancesResponseTypeDef",
    "DescribeReplicationSubnetGroupsMessagePaginateTypeDef",
    "DescribeReplicationSubnetGroupsMessageRequestTypeDef",
    "DescribeReplicationSubnetGroupsResponseTypeDef",
    "DescribeReplicationTableStatisticsMessageRequestTypeDef",
    "DescribeReplicationTableStatisticsResponseTypeDef",
    "DescribeReplicationTaskAssessmentResultsMessagePaginateTypeDef",
    "DescribeReplicationTaskAssessmentResultsMessageRequestTypeDef",
    "DescribeReplicationTaskAssessmentResultsResponseTypeDef",
    "DescribeReplicationTaskAssessmentRunsMessageRequestTypeDef",
    "DescribeReplicationTaskAssessmentRunsResponseTypeDef",
    "DescribeReplicationTaskIndividualAssessmentsMessageRequestTypeDef",
    "DescribeReplicationTaskIndividualAssessmentsResponseTypeDef",
    "DescribeReplicationTasksMessagePaginateTypeDef",
    "DescribeReplicationTasksMessageRequestTypeDef",
    "DescribeReplicationTasksMessageWaitTypeDef",
    "DescribeReplicationTasksResponseTypeDef",
    "DescribeReplicationsMessageRequestTypeDef",
    "DescribeReplicationsResponseTypeDef",
    "DescribeSchemasMessagePaginateTypeDef",
    "DescribeSchemasMessageRequestTypeDef",
    "DescribeSchemasResponseTypeDef",
    "DescribeTableStatisticsMessagePaginateTypeDef",
    "DescribeTableStatisticsMessageRequestTypeDef",
    "DescribeTableStatisticsResponseTypeDef",
    "DmsTransferSettingsTypeDef",
    "DocDbDataProviderSettingsTypeDef",
    "DocDbSettingsTypeDef",
    "DynamoDbSettingsTypeDef",
    "ElasticsearchSettingsTypeDef",
    "EmptyResponseMetadataTypeDef",
    "EndpointSettingTypeDef",
    "EndpointTypeDef",
    "EngineVersionTypeDef",
    "ErrorDetailsTypeDef",
    "EventCategoryGroupTypeDef",
    "EventSubscriptionTypeDef",
    "EventTypeDef",
    "ExportMetadataModelAssessmentMessageRequestTypeDef",
    "ExportMetadataModelAssessmentResponseTypeDef",
    "ExportMetadataModelAssessmentResultEntryTypeDef",
    "ExportSqlDetailsTypeDef",
    "FilterTypeDef",
    "FleetAdvisorLsaAnalysisResponseTypeDef",
    "FleetAdvisorSchemaObjectResponseTypeDef",
    "GcpMySQLSettingsTypeDef",
    "IBMDb2SettingsTypeDef",
    "ImportCertificateMessageRequestTypeDef",
    "ImportCertificateResponseTypeDef",
    "InstanceProfileTypeDef",
    "InventoryDataTypeDef",
    "KafkaSettingsTypeDef",
    "KerberosAuthenticationSettingsTypeDef",
    "KinesisSettingsTypeDef",
    "LimitationTypeDef",
    "ListTagsForResourceMessageRequestTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "MariaDbDataProviderSettingsTypeDef",
    "MicrosoftSQLServerSettingsTypeDef",
    "MicrosoftSqlServerDataProviderSettingsTypeDef",
    "MigrationProjectTypeDef",
    "ModifyConversionConfigurationMessageRequestTypeDef",
    "ModifyConversionConfigurationResponseTypeDef",
    "ModifyDataMigrationMessageRequestTypeDef",
    "ModifyDataMigrationResponseTypeDef",
    "ModifyDataProviderMessageRequestTypeDef",
    "ModifyDataProviderResponseTypeDef",
    "ModifyEndpointMessageRequestTypeDef",
    "ModifyEndpointResponseTypeDef",
    "ModifyEventSubscriptionMessageRequestTypeDef",
    "ModifyEventSubscriptionResponseTypeDef",
    "ModifyInstanceProfileMessageRequestTypeDef",
    "ModifyInstanceProfileResponseTypeDef",
    "ModifyMigrationProjectMessageRequestTypeDef",
    "ModifyMigrationProjectResponseTypeDef",
    "ModifyReplicationConfigMessageRequestTypeDef",
    "ModifyReplicationConfigResponseTypeDef",
    "ModifyReplicationInstanceMessageRequestTypeDef",
    "ModifyReplicationInstanceResponseTypeDef",
    "ModifyReplicationSubnetGroupMessageRequestTypeDef",
    "ModifyReplicationSubnetGroupResponseTypeDef",
    "ModifyReplicationTaskMessageRequestTypeDef",
    "ModifyReplicationTaskResponseTypeDef",
    "MongoDbDataProviderSettingsTypeDef",
    "MongoDbSettingsTypeDef",
    "MoveReplicationTaskMessageRequestTypeDef",
    "MoveReplicationTaskResponseTypeDef",
    "MySQLSettingsTypeDef",
    "MySqlDataProviderSettingsTypeDef",
    "NeptuneSettingsTypeDef",
    "OracleDataProviderSettingsTypeDef",
    "OracleSettingsOutputTypeDef",
    "OracleSettingsTypeDef",
    "OrderableReplicationInstanceTypeDef",
    "PaginatorConfigTypeDef",
    "PendingMaintenanceActionTypeDef",
    "PostgreSQLSettingsTypeDef",
    "PostgreSqlDataProviderSettingsTypeDef",
    "ProvisionDataTypeDef",
    "RdsConfigurationTypeDef",
    "RdsRecommendationTypeDef",
    "RdsRequirementsTypeDef",
    "RebootReplicationInstanceMessageRequestTypeDef",
    "RebootReplicationInstanceResponseTypeDef",
    "RecommendationDataTypeDef",
    "RecommendationSettingsTypeDef",
    "RecommendationTypeDef",
    "RedisSettingsTypeDef",
    "RedshiftDataProviderSettingsTypeDef",
    "RedshiftSettingsTypeDef",
    "RefreshSchemasMessageRequestTypeDef",
    "RefreshSchemasResponseTypeDef",
    "RefreshSchemasStatusTypeDef",
    "ReloadReplicationTablesMessageRequestTypeDef",
    "ReloadReplicationTablesResponseTypeDef",
    "ReloadTablesMessageRequestTypeDef",
    "ReloadTablesResponseTypeDef",
    "RemoveTagsFromResourceMessageRequestTypeDef",
    "ReplicationConfigTypeDef",
    "ReplicationInstanceTaskLogTypeDef",
    "ReplicationInstanceTypeDef",
    "ReplicationPendingModifiedValuesTypeDef",
    "ReplicationStatsTypeDef",
    "ReplicationSubnetGroupTypeDef",
    "ReplicationTaskAssessmentResultTypeDef",
    "ReplicationTaskAssessmentRunProgressTypeDef",
    "ReplicationTaskAssessmentRunResultStatisticTypeDef",
    "ReplicationTaskAssessmentRunTypeDef",
    "ReplicationTaskIndividualAssessmentTypeDef",
    "ReplicationTaskStatsTypeDef",
    "ReplicationTaskTypeDef",
    "ReplicationTypeDef",
    "ResourcePendingMaintenanceActionsTypeDef",
    "ResponseMetadataTypeDef",
    "RunFleetAdvisorLsaAnalysisResponseTypeDef",
    "S3SettingsTypeDef",
    "SCApplicationAttributesTypeDef",
    "SchemaConversionRequestTypeDef",
    "SchemaResponseTypeDef",
    "SchemaShortInfoResponseTypeDef",
    "ServerShortInfoResponseTypeDef",
    "SourceDataSettingOutputTypeDef",
    "SourceDataSettingTypeDef",
    "SourceDataSettingUnionTypeDef",
    "StartDataMigrationMessageRequestTypeDef",
    "StartDataMigrationResponseTypeDef",
    "StartExtensionPackAssociationMessageRequestTypeDef",
    "StartExtensionPackAssociationResponseTypeDef",
    "StartMetadataModelAssessmentMessageRequestTypeDef",
    "StartMetadataModelAssessmentResponseTypeDef",
    "StartMetadataModelConversionMessageRequestTypeDef",
    "StartMetadataModelConversionResponseTypeDef",
    "StartMetadataModelExportAsScriptMessageRequestTypeDef",
    "StartMetadataModelExportAsScriptResponseTypeDef",
    "StartMetadataModelExportToTargetMessageRequestTypeDef",
    "StartMetadataModelExportToTargetResponseTypeDef",
    "StartMetadataModelImportMessageRequestTypeDef",
    "StartMetadataModelImportResponseTypeDef",
    "StartRecommendationsRequestEntryTypeDef",
    "StartRecommendationsRequestRequestTypeDef",
    "StartReplicationMessageRequestTypeDef",
    "StartReplicationResponseTypeDef",
    "StartReplicationTaskAssessmentMessageRequestTypeDef",
    "StartReplicationTaskAssessmentResponseTypeDef",
    "StartReplicationTaskAssessmentRunMessageRequestTypeDef",
    "StartReplicationTaskAssessmentRunResponseTypeDef",
    "StartReplicationTaskMessageRequestTypeDef",
    "StartReplicationTaskResponseTypeDef",
    "StopDataMigrationMessageRequestTypeDef",
    "StopDataMigrationResponseTypeDef",
    "StopReplicationMessageRequestTypeDef",
    "StopReplicationResponseTypeDef",
    "StopReplicationTaskMessageRequestTypeDef",
    "StopReplicationTaskResponseTypeDef",
    "SubnetTypeDef",
    "SupportedEndpointTypeTypeDef",
    "SybaseSettingsTypeDef",
    "TableStatisticsTypeDef",
    "TableToReloadTypeDef",
    "TagTypeDef",
    "TestConnectionMessageRequestTypeDef",
    "TestConnectionResponseTypeDef",
    "TimestampTypeDef",
    "TimestreamSettingsTypeDef",
    "UpdateSubscriptionsToEventBridgeMessageRequestTypeDef",
    "UpdateSubscriptionsToEventBridgeResponseTypeDef",
    "VpcSecurityGroupMembershipTypeDef",
    "WaiterConfigTypeDef",
)


class AccountQuotaTypeDef(TypedDict):
    AccountQuotaName: NotRequired[str]
    Used: NotRequired[int]
    Max: NotRequired[int]


class TagTypeDef(TypedDict):
    Key: NotRequired[str]
    Value: NotRequired[str]
    ResourceArn: NotRequired[str]


class ApplyPendingMaintenanceActionMessageRequestTypeDef(TypedDict):
    ReplicationInstanceArn: str
    ApplyAction: str
    OptInType: str


class ResponseMetadataTypeDef(TypedDict):
    RequestId: str
    HTTPStatusCode: int
    HTTPHeaders: Dict[str, str]
    RetryAttempts: int
    HostId: NotRequired[str]


class AvailabilityZoneTypeDef(TypedDict):
    Name: NotRequired[str]


class BatchStartRecommendationsErrorEntryTypeDef(TypedDict):
    DatabaseId: NotRequired[str]
    Message: NotRequired[str]
    Code: NotRequired[str]


BlobTypeDef = Union[str, bytes, IO[Any], StreamingBody]


class CancelReplicationTaskAssessmentRunMessageRequestTypeDef(TypedDict):
    ReplicationTaskAssessmentRunArn: str


class CertificateTypeDef(TypedDict):
    CertificateIdentifier: NotRequired[str]
    CertificateCreationDate: NotRequired[datetime]
    CertificatePem: NotRequired[str]
    CertificateWallet: NotRequired[bytes]
    CertificateArn: NotRequired[str]
    CertificateOwner: NotRequired[str]
    ValidFromDate: NotRequired[datetime]
    ValidToDate: NotRequired[datetime]
    SigningAlgorithm: NotRequired[str]
    KeyLength: NotRequired[int]


class CollectorHealthCheckTypeDef(TypedDict):
    CollectorStatus: NotRequired[CollectorStatusType]
    LocalCollectorS3Access: NotRequired[bool]
    WebCollectorS3Access: NotRequired[bool]
    WebCollectorGrantedRoleBasedAccess: NotRequired[bool]


class InventoryDataTypeDef(TypedDict):
    NumberOfDatabases: NotRequired[int]
    NumberOfSchemas: NotRequired[int]


class CollectorShortInfoResponseTypeDef(TypedDict):
    CollectorReferencedId: NotRequired[str]
    CollectorName: NotRequired[str]


class ComputeConfigOutputTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    DnsNameServers: NotRequired[str]
    KmsKeyId: NotRequired[str]
    MaxCapacityUnits: NotRequired[int]
    MinCapacityUnits: NotRequired[int]
    MultiAZ: NotRequired[bool]
    PreferredMaintenanceWindow: NotRequired[str]
    ReplicationSubnetGroupId: NotRequired[str]
    VpcSecurityGroupIds: NotRequired[List[str]]


class ComputeConfigTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    DnsNameServers: NotRequired[str]
    KmsKeyId: NotRequired[str]
    MaxCapacityUnits: NotRequired[int]
    MinCapacityUnits: NotRequired[int]
    MultiAZ: NotRequired[bool]
    PreferredMaintenanceWindow: NotRequired[str]
    ReplicationSubnetGroupId: NotRequired[str]
    VpcSecurityGroupIds: NotRequired[Sequence[str]]


class ConnectionTypeDef(TypedDict):
    ReplicationInstanceArn: NotRequired[str]
    EndpointArn: NotRequired[str]
    Status: NotRequired[str]
    LastFailureMessage: NotRequired[str]
    EndpointIdentifier: NotRequired[str]
    ReplicationInstanceIdentifier: NotRequired[str]


class DmsTransferSettingsTypeDef(TypedDict):
    ServiceAccessRoleArn: NotRequired[str]
    BucketName: NotRequired[str]


class DocDbSettingsTypeDef(TypedDict):
    Username: NotRequired[str]
    Password: NotRequired[str]
    ServerName: NotRequired[str]
    Port: NotRequired[int]
    DatabaseName: NotRequired[str]
    NestingLevel: NotRequired[NestingLevelValueType]
    ExtractDocId: NotRequired[bool]
    DocsToInvestigate: NotRequired[int]
    KmsKeyId: NotRequired[str]
    SecretsManagerAccessRoleArn: NotRequired[str]
    SecretsManagerSecretId: NotRequired[str]
    UseUpdateLookUp: NotRequired[bool]
    ReplicateShardCollections: NotRequired[bool]


class DynamoDbSettingsTypeDef(TypedDict):
    ServiceAccessRoleArn: str


class ElasticsearchSettingsTypeDef(TypedDict):
    ServiceAccessRoleArn: str
    EndpointUri: str
    FullLoadErrorPercentage: NotRequired[int]
    ErrorRetryDuration: NotRequired[int]
    UseNewMappingType: NotRequired[bool]


class GcpMySQLSettingsTypeDef(TypedDict):
    AfterConnectScript: NotRequired[str]
    CleanSourceMetadataOnMismatch: NotRequired[bool]
    DatabaseName: NotRequired[str]
    EventsPollInterval: NotRequired[int]
    TargetDbType: NotRequired[TargetDbTypeType]
    MaxFileSize: NotRequired[int]
    ParallelLoadThreads: NotRequired[int]
    Password: NotRequired[str]
    Port: NotRequired[int]
    ServerName: NotRequired[str]
    ServerTimezone: NotRequired[str]
    Username: NotRequired[str]
    SecretsManagerAccessRoleArn: NotRequired[str]
    SecretsManagerSecretId: NotRequired[str]


class IBMDb2SettingsTypeDef(TypedDict):
    DatabaseName: NotRequired[str]
    Password: NotRequired[str]
    Port: NotRequired[int]
    ServerName: NotRequired[str]
    SetDataCaptureChanges: NotRequired[bool]
    CurrentLsn: NotRequired[str]
    MaxKBytesPerRead: NotRequired[int]
    Username: NotRequired[str]
    SecretsManagerAccessRoleArn: NotRequired[str]
    SecretsManagerSecretId: NotRequired[str]
    LoadTimeout: NotRequired[int]
    WriteBufferSize: NotRequired[int]
    MaxFileSize: NotRequired[int]
    KeepCsvFiles: NotRequired[bool]


class KafkaSettingsTypeDef(TypedDict):
    Broker: NotRequired[str]
    Topic: NotRequired[str]
    MessageFormat: NotRequired[MessageFormatValueType]
    IncludeTransactionDetails: NotRequired[bool]
    IncludePartitionValue: NotRequired[bool]
    PartitionIncludeSchemaTable: NotRequired[bool]
    IncludeTableAlterOperations: NotRequired[bool]
    IncludeControlDetails: NotRequired[bool]
    MessageMaxBytes: NotRequired[int]
    IncludeNullAndEmpty: NotRequired[bool]
    SecurityProtocol: NotRequired[KafkaSecurityProtocolType]
    SslClientCertificateArn: NotRequired[str]
    SslClientKeyArn: NotRequired[str]
    SslClientKeyPassword: NotRequired[str]
    SslCaCertificateArn: NotRequired[str]
    SaslUsername: NotRequired[str]
    SaslPassword: NotRequired[str]
    NoHexPrefix: NotRequired[bool]
    SaslMechanism: NotRequired[KafkaSaslMechanismType]
    SslEndpointIdentificationAlgorithm: NotRequired[KafkaSslEndpointIdentificationAlgorithmType]
    UseLargeIntegerValue: NotRequired[bool]


class KinesisSettingsTypeDef(TypedDict):
    StreamArn: NotRequired[str]
    MessageFormat: NotRequired[MessageFormatValueType]
    ServiceAccessRoleArn: NotRequired[str]
    IncludeTransactionDetails: NotRequired[bool]
    IncludePartitionValue: NotRequired[bool]
    PartitionIncludeSchemaTable: NotRequired[bool]
    IncludeTableAlterOperations: NotRequired[bool]
    IncludeControlDetails: NotRequired[bool]
    IncludeNullAndEmpty: NotRequired[bool]
    NoHexPrefix: NotRequired[bool]
    UseLargeIntegerValue: NotRequired[bool]


class MicrosoftSQLServerSettingsTypeDef(TypedDict):
    Port: NotRequired[int]
    BcpPacketSize: NotRequired[int]
    DatabaseName: NotRequired[str]
    ControlTablesFileGroup: NotRequired[str]
    Password: NotRequired[str]
    QuerySingleAlwaysOnNode: NotRequired[bool]
    ReadBackupOnly: NotRequired[bool]
    SafeguardPolicy: NotRequired[SafeguardPolicyType]
    ServerName: NotRequired[str]
    Username: NotRequired[str]
    UseBcpFullLoad: NotRequired[bool]
    UseThirdPartyBackupDevice: NotRequired[bool]
    SecretsManagerAccessRoleArn: NotRequired[str]
    SecretsManagerSecretId: NotRequired[str]
    TrimSpaceInChar: NotRequired[bool]
    TlogAccessMode: NotRequired[TlogAccessModeType]
    ForceLobLookup: NotRequired[bool]
    AuthenticationMethod: NotRequired[SqlServerAuthenticationMethodType]


class MongoDbSettingsTypeDef(TypedDict):
    Username: NotRequired[str]
    Password: NotRequired[str]
    ServerName: NotRequired[str]
    Port: NotRequired[int]
    DatabaseName: NotRequired[str]
    AuthType: NotRequired[AuthTypeValueType]
    AuthMechanism: NotRequired[AuthMechanismValueType]
    NestingLevel: NotRequired[NestingLevelValueType]
    ExtractDocId: NotRequired[str]
    DocsToInvestigate: NotRequired[str]
    AuthSource: NotRequired[str]
    KmsKeyId: NotRequired[str]
    SecretsManagerAccessRoleArn: NotRequired[str]
    SecretsManagerSecretId: NotRequired[str]
    UseUpdateLookUp: NotRequired[bool]
    ReplicateShardCollections: NotRequired[bool]


class MySQLSettingsTypeDef(TypedDict):
    AfterConnectScript: NotRequired[str]
    CleanSourceMetadataOnMismatch: NotRequired[bool]
    DatabaseName: NotRequired[str]
    EventsPollInterval: NotRequired[int]
    TargetDbType: NotRequired[TargetDbTypeType]
    MaxFileSize: NotRequired[int]
    ParallelLoadThreads: NotRequired[int]
    Password: NotRequired[str]
    Port: NotRequired[int]
    ServerName: NotRequired[str]
    ServerTimezone: NotRequired[str]
    Username: NotRequired[str]
    SecretsManagerAccessRoleArn: NotRequired[str]
    SecretsManagerSecretId: NotRequired[str]
    ExecuteTimeout: NotRequired[int]


class NeptuneSettingsTypeDef(TypedDict):
    S3BucketName: str
    S3BucketFolder: str
    ServiceAccessRoleArn: NotRequired[str]
    ErrorRetryDuration: NotRequired[int]
    MaxFileSize: NotRequired[int]
    MaxRetryCount: NotRequired[int]
    IamAuthEnabled: NotRequired[bool]


class OracleSettingsTypeDef(TypedDict):
    AddSupplementalLogging: NotRequired[bool]
    ArchivedLogDestId: NotRequired[int]
    AdditionalArchivedLogDestId: NotRequired[int]
    ExtraArchivedLogDestIds: NotRequired[Sequence[int]]
    AllowSelectNestedTables: NotRequired[bool]
    ParallelAsmReadThreads: NotRequired[int]
    ReadAheadBlocks: NotRequired[int]
    AccessAlternateDirectly: NotRequired[bool]
    UseAlternateFolderForOnline: NotRequired[bool]
    OraclePathPrefix: NotRequired[str]
    UsePathPrefix: NotRequired[str]
    ReplacePathPrefix: NotRequired[bool]
    EnableHomogenousTablespace: NotRequired[bool]
    DirectPathNoLog: NotRequired[bool]
    ArchivedLogsOnly: NotRequired[bool]
    AsmPassword: NotRequired[str]
    AsmServer: NotRequired[str]
    AsmUser: NotRequired[str]
    CharLengthSemantics: NotRequired[CharLengthSemanticsType]
    DatabaseName: NotRequired[str]
    DirectPathParallelLoad: NotRequired[bool]
    FailTasksOnLobTruncation: NotRequired[bool]
    NumberDatatypeScale: NotRequired[int]
    Password: NotRequired[str]
    Port: NotRequired[int]
    ReadTableSpaceName: NotRequired[bool]
    RetryInterval: NotRequired[int]
    SecurityDbEncryption: NotRequired[str]
    SecurityDbEncryptionName: NotRequired[str]
    ServerName: NotRequired[str]
    SpatialDataOptionToGeoJsonFunctionName: NotRequired[str]
    StandbyDelayTime: NotRequired[int]
    Username: NotRequired[str]
    UseBFile: NotRequired[bool]
    UseDirectPathFullLoad: NotRequired[bool]
    UseLogminerReader: NotRequired[bool]
    SecretsManagerAccessRoleArn: NotRequired[str]
    SecretsManagerSecretId: NotRequired[str]
    SecretsManagerOracleAsmAccessRoleArn: NotRequired[str]
    SecretsManagerOracleAsmSecretId: NotRequired[str]
    TrimSpaceInChar: NotRequired[bool]
    ConvertTimestampWithZoneToUTC: NotRequired[bool]
    OpenTransactionWindow: NotRequired[int]
    AuthenticationMethod: NotRequired[OracleAuthenticationMethodType]


class PostgreSQLSettingsTypeDef(TypedDict):
    AfterConnectScript: NotRequired[str]
    CaptureDdls: NotRequired[bool]
    MaxFileSize: NotRequired[int]
    DatabaseName: NotRequired[str]
    DdlArtifactsSchema: NotRequired[str]
    ExecuteTimeout: NotRequired[int]
    FailTasksOnLobTruncation: NotRequired[bool]
    HeartbeatEnable: NotRequired[bool]
    HeartbeatSchema: NotRequired[str]
    HeartbeatFrequency: NotRequired[int]
    Password: NotRequired[str]
    Port: NotRequired[int]
    ServerName: NotRequired[str]
    Username: NotRequired[str]
    SlotName: NotRequired[str]
    PluginName: NotRequired[PluginNameValueType]
    SecretsManagerAccessRoleArn: NotRequired[str]
    SecretsManagerSecretId: NotRequired[str]
    TrimSpaceInChar: NotRequired[bool]
    MapBooleanAsBoolean: NotRequired[bool]
    MapJsonbAsClob: NotRequired[bool]
    MapLongVarcharAs: NotRequired[LongVarcharMappingTypeType]
    DatabaseMode: NotRequired[DatabaseModeType]
    BabelfishDatabaseName: NotRequired[str]
    DisableUnicodeSourceFilter: NotRequired[bool]


class RedisSettingsTypeDef(TypedDict):
    ServerName: str
    Port: int
    SslSecurityProtocol: NotRequired[SslSecurityProtocolValueType]
    AuthType: NotRequired[RedisAuthTypeValueType]
    AuthUserName: NotRequired[str]
    AuthPassword: NotRequired[str]
    SslCaCertificateArn: NotRequired[str]


class RedshiftSettingsTypeDef(TypedDict):
    AcceptAnyDate: NotRequired[bool]
    AfterConnectScript: NotRequired[str]
    BucketFolder: NotRequired[str]
    BucketName: NotRequired[str]
    CaseSensitiveNames: NotRequired[bool]
    CompUpdate: NotRequired[bool]
    ConnectionTimeout: NotRequired[int]
    DatabaseName: NotRequired[str]
    DateFormat: NotRequired[str]
    EmptyAsNull: NotRequired[bool]
    EncryptionMode: NotRequired[EncryptionModeValueType]
    ExplicitIds: NotRequired[bool]
    FileTransferUploadStreams: NotRequired[int]
    LoadTimeout: NotRequired[int]
    MaxFileSize: NotRequired[int]
    Password: NotRequired[str]
    Port: NotRequired[int]
    RemoveQuotes: NotRequired[bool]
    ReplaceInvalidChars: NotRequired[str]
    ReplaceChars: NotRequired[str]
    ServerName: NotRequired[str]
    ServiceAccessRoleArn: NotRequired[str]
    ServerSideEncryptionKmsKeyId: NotRequired[str]
    TimeFormat: NotRequired[str]
    TrimBlanks: NotRequired[bool]
    TruncateColumns: NotRequired[bool]
    Username: NotRequired[str]
    WriteBufferSize: NotRequired[int]
    SecretsManagerAccessRoleArn: NotRequired[str]
    SecretsManagerSecretId: NotRequired[str]
    MapBooleanAsBoolean: NotRequired[bool]


class S3SettingsTypeDef(TypedDict):
    ServiceAccessRoleArn: NotRequired[str]
    ExternalTableDefinition: NotRequired[str]
    CsvRowDelimiter: NotRequired[str]
    CsvDelimiter: NotRequired[str]
    BucketFolder: NotRequired[str]
    BucketName: NotRequired[str]
    CompressionType: NotRequired[CompressionTypeValueType]
    EncryptionMode: NotRequired[EncryptionModeValueType]
    ServerSideEncryptionKmsKeyId: NotRequired[str]
    DataFormat: NotRequired[DataFormatValueType]
    EncodingType: NotRequired[EncodingTypeValueType]
    DictPageSizeLimit: NotRequired[int]
    RowGroupLength: NotRequired[int]
    DataPageSize: NotRequired[int]
    ParquetVersion: NotRequired[ParquetVersionValueType]
    EnableStatistics: NotRequired[bool]
    IncludeOpForFullLoad: NotRequired[bool]
    CdcInsertsOnly: NotRequired[bool]
    TimestampColumnName: NotRequired[str]
    ParquetTimestampInMillisecond: NotRequired[bool]
    CdcInsertsAndUpdates: NotRequired[bool]
    DatePartitionEnabled: NotRequired[bool]
    DatePartitionSequence: NotRequired[DatePartitionSequenceValueType]
    DatePartitionDelimiter: NotRequired[DatePartitionDelimiterValueType]
    UseCsvNoSupValue: NotRequired[bool]
    CsvNoSupValue: NotRequired[str]
    PreserveTransactions: NotRequired[bool]
    CdcPath: NotRequired[str]
    UseTaskStartTimeForFullLoadTimestamp: NotRequired[bool]
    CannedAclForObjects: NotRequired[CannedAclForObjectsValueType]
    AddColumnName: NotRequired[bool]
    CdcMaxBatchInterval: NotRequired[int]
    CdcMinFileSize: NotRequired[int]
    CsvNullValue: NotRequired[str]
    IgnoreHeaderRows: NotRequired[int]
    MaxFileSize: NotRequired[int]
    Rfc4180: NotRequired[bool]
    DatePartitionTimezone: NotRequired[str]
    AddTrailingPaddingCharacter: NotRequired[bool]
    ExpectedBucketOwner: NotRequired[str]
    GlueCatalogGeneration: NotRequired[bool]


class SybaseSettingsTypeDef(TypedDict):
    DatabaseName: NotRequired[str]
    Password: NotRequired[str]
    Port: NotRequired[int]
    ServerName: NotRequired[str]
    Username: NotRequired[str]
    SecretsManagerAccessRoleArn: NotRequired[str]
    SecretsManagerSecretId: NotRequired[str]


class TimestreamSettingsTypeDef(TypedDict):
    DatabaseName: str
    MemoryDuration: int
    MagneticDuration: int
    CdcInsertsAndUpdates: NotRequired[bool]
    EnableMagneticStoreWrites: NotRequired[bool]


class EventSubscriptionTypeDef(TypedDict):
    CustomerAwsId: NotRequired[str]
    CustSubscriptionId: NotRequired[str]
    SnsTopicArn: NotRequired[str]
    Status: NotRequired[str]
    SubscriptionCreationTime: NotRequired[str]
    SourceType: NotRequired[str]
    SourceIdsList: NotRequired[List[str]]
    EventCategoriesList: NotRequired[List[str]]
    Enabled: NotRequired[bool]


class CreateFleetAdvisorCollectorRequestRequestTypeDef(TypedDict):
    CollectorName: str
    ServiceAccessRoleArn: str
    S3BucketName: str
    Description: NotRequired[str]


class InstanceProfileTypeDef(TypedDict):
    InstanceProfileArn: NotRequired[str]
    AvailabilityZone: NotRequired[str]
    KmsKeyArn: NotRequired[str]
    PubliclyAccessible: NotRequired[bool]
    NetworkType: NotRequired[str]
    InstanceProfileName: NotRequired[str]
    Description: NotRequired[str]
    InstanceProfileCreationTime: NotRequired[datetime]
    SubnetGroupIdentifier: NotRequired[str]
    VpcSecurityGroups: NotRequired[List[str]]


class DataProviderDescriptorDefinitionTypeDef(TypedDict):
    DataProviderIdentifier: str
    SecretsManagerSecretId: NotRequired[str]
    SecretsManagerAccessRoleArn: NotRequired[str]


class SCApplicationAttributesTypeDef(TypedDict):
    S3BucketPath: NotRequired[str]
    S3BucketRoleArn: NotRequired[str]


class KerberosAuthenticationSettingsTypeDef(TypedDict):
    KeyCacheSecretId: NotRequired[str]
    KeyCacheSecretIamArn: NotRequired[str]
    Krb5FileContents: NotRequired[str]


TimestampTypeDef = Union[datetime, str]


class DataMigrationSettingsTypeDef(TypedDict):
    NumberOfJobs: NotRequired[int]
    CloudwatchLogsEnabled: NotRequired[bool]
    SelectionRules: NotRequired[str]


class DataMigrationStatisticsTypeDef(TypedDict):
    TablesLoaded: NotRequired[int]
    ElapsedTimeMillis: NotRequired[int]
    TablesLoading: NotRequired[int]
    FullLoadPercentage: NotRequired[int]
    CDCLatency: NotRequired[int]
    TablesQueued: NotRequired[int]
    TablesErrored: NotRequired[int]
    StartTime: NotRequired[datetime]
    StopTime: NotRequired[datetime]


class SourceDataSettingOutputTypeDef(TypedDict):
    CDCStartPosition: NotRequired[str]
    CDCStartTime: NotRequired[datetime]
    CDCStopTime: NotRequired[datetime]
    SlotName: NotRequired[str]


class DataProviderDescriptorTypeDef(TypedDict):
    SecretsManagerSecretId: NotRequired[str]
    SecretsManagerAccessRoleArn: NotRequired[str]
    DataProviderName: NotRequired[str]
    DataProviderArn: NotRequired[str]


class DocDbDataProviderSettingsTypeDef(TypedDict):
    ServerName: NotRequired[str]
    Port: NotRequired[int]
    DatabaseName: NotRequired[str]
    SslMode: NotRequired[DmsSslModeValueType]
    CertificateArn: NotRequired[str]


class MariaDbDataProviderSettingsTypeDef(TypedDict):
    ServerName: NotRequired[str]
    Port: NotRequired[int]
    SslMode: NotRequired[DmsSslModeValueType]
    CertificateArn: NotRequired[str]


class MicrosoftSqlServerDataProviderSettingsTypeDef(TypedDict):
    ServerName: NotRequired[str]
    Port: NotRequired[int]
    DatabaseName: NotRequired[str]
    SslMode: NotRequired[DmsSslModeValueType]
    CertificateArn: NotRequired[str]


class MongoDbDataProviderSettingsTypeDef(TypedDict):
    ServerName: NotRequired[str]
    Port: NotRequired[int]
    DatabaseName: NotRequired[str]
    SslMode: NotRequired[DmsSslModeValueType]
    CertificateArn: NotRequired[str]
    AuthType: NotRequired[AuthTypeValueType]
    AuthSource: NotRequired[str]
    AuthMechanism: NotRequired[AuthMechanismValueType]


class MySqlDataProviderSettingsTypeDef(TypedDict):
    ServerName: NotRequired[str]
    Port: NotRequired[int]
    SslMode: NotRequired[DmsSslModeValueType]
    CertificateArn: NotRequired[str]


class OracleDataProviderSettingsTypeDef(TypedDict):
    ServerName: NotRequired[str]
    Port: NotRequired[int]
    DatabaseName: NotRequired[str]
    SslMode: NotRequired[DmsSslModeValueType]
    CertificateArn: NotRequired[str]
    AsmServer: NotRequired[str]
    SecretsManagerOracleAsmSecretId: NotRequired[str]
    SecretsManagerOracleAsmAccessRoleArn: NotRequired[str]
    SecretsManagerSecurityDbEncryptionSecretId: NotRequired[str]
    SecretsManagerSecurityDbEncryptionAccessRoleArn: NotRequired[str]


class PostgreSqlDataProviderSettingsTypeDef(TypedDict):
    ServerName: NotRequired[str]
    Port: NotRequired[int]
    DatabaseName: NotRequired[str]
    SslMode: NotRequired[DmsSslModeValueType]
    CertificateArn: NotRequired[str]


class RedshiftDataProviderSettingsTypeDef(TypedDict):
    ServerName: NotRequired[str]
    Port: NotRequired[int]
    DatabaseName: NotRequired[str]


class DatabaseInstanceSoftwareDetailsResponseTypeDef(TypedDict):
    Engine: NotRequired[str]
    EngineVersion: NotRequired[str]
    EngineEdition: NotRequired[str]
    ServicePack: NotRequired[str]
    SupportLevel: NotRequired[str]
    OsArchitecture: NotRequired[int]
    Tooltip: NotRequired[str]


class ServerShortInfoResponseTypeDef(TypedDict):
    ServerId: NotRequired[str]
    IpAddress: NotRequired[str]
    ServerName: NotRequired[str]


class DatabaseShortInfoResponseTypeDef(TypedDict):
    DatabaseId: NotRequired[str]
    DatabaseName: NotRequired[str]
    DatabaseIpAddress: NotRequired[str]
    DatabaseEngine: NotRequired[str]


class DefaultErrorDetailsTypeDef(TypedDict):
    Message: NotRequired[str]


class DeleteCertificateMessageRequestTypeDef(TypedDict):
    CertificateArn: str


class DeleteCollectorRequestRequestTypeDef(TypedDict):
    CollectorReferencedId: str


class DeleteConnectionMessageRequestTypeDef(TypedDict):
    EndpointArn: str
    ReplicationInstanceArn: str


class DeleteDataMigrationMessageRequestTypeDef(TypedDict):
    DataMigrationIdentifier: str


class DeleteDataProviderMessageRequestTypeDef(TypedDict):
    DataProviderIdentifier: str


class DeleteEndpointMessageRequestTypeDef(TypedDict):
    EndpointArn: str


class DeleteEventSubscriptionMessageRequestTypeDef(TypedDict):
    SubscriptionName: str


class DeleteFleetAdvisorDatabasesRequestRequestTypeDef(TypedDict):
    DatabaseIds: Sequence[str]


class DeleteInstanceProfileMessageRequestTypeDef(TypedDict):
    InstanceProfileIdentifier: str


class DeleteMigrationProjectMessageRequestTypeDef(TypedDict):
    MigrationProjectIdentifier: str


class DeleteReplicationConfigMessageRequestTypeDef(TypedDict):
    ReplicationConfigArn: str


class DeleteReplicationInstanceMessageRequestTypeDef(TypedDict):
    ReplicationInstanceArn: str


class DeleteReplicationSubnetGroupMessageRequestTypeDef(TypedDict):
    ReplicationSubnetGroupIdentifier: str


class DeleteReplicationTaskAssessmentRunMessageRequestTypeDef(TypedDict):
    ReplicationTaskAssessmentRunArn: str


class DeleteReplicationTaskMessageRequestTypeDef(TypedDict):
    ReplicationTaskArn: str


class DescribeApplicableIndividualAssessmentsMessageRequestTypeDef(TypedDict):
    ReplicationTaskArn: NotRequired[str]
    ReplicationInstanceArn: NotRequired[str]
    SourceEngineName: NotRequired[str]
    TargetEngineName: NotRequired[str]
    MigrationType: NotRequired[MigrationTypeValueType]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class FilterTypeDef(TypedDict):
    Name: str
    Values: Sequence[str]


class PaginatorConfigTypeDef(TypedDict):
    MaxItems: NotRequired[int]
    PageSize: NotRequired[int]
    StartingToken: NotRequired[str]


class WaiterConfigTypeDef(TypedDict):
    Delay: NotRequired[int]
    MaxAttempts: NotRequired[int]


class DescribeConversionConfigurationMessageRequestTypeDef(TypedDict):
    MigrationProjectIdentifier: str


class DescribeEndpointSettingsMessageRequestTypeDef(TypedDict):
    EngineName: str
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


EndpointSettingTypeDef = TypedDict(
    "EndpointSettingTypeDef",
    {
        "Name": NotRequired[str],
        "Type": NotRequired[EndpointSettingTypeValueType],
        "EnumValues": NotRequired[List[str]],
        "Sensitive": NotRequired[bool],
        "Units": NotRequired[str],
        "Applicability": NotRequired[str],
        "IntValueMin": NotRequired[int],
        "IntValueMax": NotRequired[int],
        "DefaultValue": NotRequired[str],
    },
)


class SupportedEndpointTypeTypeDef(TypedDict):
    EngineName: NotRequired[str]
    SupportsCDC: NotRequired[bool]
    EndpointType: NotRequired[ReplicationEndpointTypeValueType]
    ReplicationInstanceEngineMinimumVersion: NotRequired[str]
    EngineDisplayName: NotRequired[str]


class DescribeEngineVersionsMessageRequestTypeDef(TypedDict):
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class EngineVersionTypeDef(TypedDict):
    Version: NotRequired[str]
    Lifecycle: NotRequired[str]
    ReleaseStatus: NotRequired[ReleaseStatusValuesType]
    LaunchDate: NotRequired[datetime]
    AutoUpgradeDate: NotRequired[datetime]
    DeprecationDate: NotRequired[datetime]
    ForceUpgradeDate: NotRequired[datetime]
    AvailableUpgrades: NotRequired[List[str]]


class EventCategoryGroupTypeDef(TypedDict):
    SourceType: NotRequired[str]
    EventCategories: NotRequired[List[str]]


class EventTypeDef(TypedDict):
    SourceIdentifier: NotRequired[str]
    SourceType: NotRequired[Literal["replication-instance"]]
    Message: NotRequired[str]
    EventCategories: NotRequired[List[str]]
    Date: NotRequired[datetime]


class DescribeFleetAdvisorLsaAnalysisRequestRequestTypeDef(TypedDict):
    MaxRecords: NotRequired[int]
    NextToken: NotRequired[str]


class FleetAdvisorLsaAnalysisResponseTypeDef(TypedDict):
    LsaAnalysisId: NotRequired[str]
    Status: NotRequired[str]


class FleetAdvisorSchemaObjectResponseTypeDef(TypedDict):
    SchemaId: NotRequired[str]
    ObjectType: NotRequired[str]
    NumberOfObjects: NotRequired[int]
    CodeLineCount: NotRequired[int]
    CodeSize: NotRequired[int]


class DescribeOrderableReplicationInstancesMessageRequestTypeDef(TypedDict):
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class OrderableReplicationInstanceTypeDef(TypedDict):
    EngineVersion: NotRequired[str]
    ReplicationInstanceClass: NotRequired[str]
    StorageType: NotRequired[str]
    MinAllocatedStorage: NotRequired[int]
    MaxAllocatedStorage: NotRequired[int]
    DefaultAllocatedStorage: NotRequired[int]
    IncludedAllocatedStorage: NotRequired[int]
    AvailabilityZones: NotRequired[List[str]]
    ReleaseStatus: NotRequired[ReleaseStatusValuesType]


LimitationTypeDef = TypedDict(
    "LimitationTypeDef",
    {
        "DatabaseId": NotRequired[str],
        "EngineName": NotRequired[str],
        "Name": NotRequired[str],
        "Description": NotRequired[str],
        "Impact": NotRequired[str],
        "Type": NotRequired[str],
    },
)


class DescribeRefreshSchemasStatusMessageRequestTypeDef(TypedDict):
    EndpointArn: str


class RefreshSchemasStatusTypeDef(TypedDict):
    EndpointArn: NotRequired[str]
    ReplicationInstanceArn: NotRequired[str]
    Status: NotRequired[RefreshSchemasStatusTypeValueType]
    LastRefreshDate: NotRequired[datetime]
    LastFailureMessage: NotRequired[str]


class DescribeReplicationInstanceTaskLogsMessageRequestTypeDef(TypedDict):
    ReplicationInstanceArn: str
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class ReplicationInstanceTaskLogTypeDef(TypedDict):
    ReplicationTaskName: NotRequired[str]
    ReplicationTaskArn: NotRequired[str]
    ReplicationInstanceTaskLogSize: NotRequired[int]


class TableStatisticsTypeDef(TypedDict):
    SchemaName: NotRequired[str]
    TableName: NotRequired[str]
    Inserts: NotRequired[int]
    Deletes: NotRequired[int]
    Updates: NotRequired[int]
    Ddls: NotRequired[int]
    AppliedInserts: NotRequired[int]
    AppliedDeletes: NotRequired[int]
    AppliedUpdates: NotRequired[int]
    AppliedDdls: NotRequired[int]
    FullLoadRows: NotRequired[int]
    FullLoadCondtnlChkFailedRows: NotRequired[int]
    FullLoadErrorRows: NotRequired[int]
    FullLoadStartTime: NotRequired[datetime]
    FullLoadEndTime: NotRequired[datetime]
    FullLoadReloaded: NotRequired[bool]
    LastUpdateTime: NotRequired[datetime]
    TableState: NotRequired[str]
    ValidationPendingRecords: NotRequired[int]
    ValidationFailedRecords: NotRequired[int]
    ValidationSuspendedRecords: NotRequired[int]
    ValidationState: NotRequired[str]
    ValidationStateDetails: NotRequired[str]


class DescribeReplicationTaskAssessmentResultsMessageRequestTypeDef(TypedDict):
    ReplicationTaskArn: NotRequired[str]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class ReplicationTaskAssessmentResultTypeDef(TypedDict):
    ReplicationTaskIdentifier: NotRequired[str]
    ReplicationTaskArn: NotRequired[str]
    ReplicationTaskLastAssessmentDate: NotRequired[datetime]
    AssessmentStatus: NotRequired[str]
    AssessmentResultsFile: NotRequired[str]
    AssessmentResults: NotRequired[str]
    S3ObjectUrl: NotRequired[str]


class ReplicationTaskIndividualAssessmentTypeDef(TypedDict):
    ReplicationTaskIndividualAssessmentArn: NotRequired[str]
    ReplicationTaskAssessmentRunArn: NotRequired[str]
    IndividualAssessmentName: NotRequired[str]
    Status: NotRequired[str]
    ReplicationTaskIndividualAssessmentStartDate: NotRequired[datetime]


class DescribeSchemasMessageRequestTypeDef(TypedDict):
    EndpointArn: str
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class OracleSettingsOutputTypeDef(TypedDict):
    AddSupplementalLogging: NotRequired[bool]
    ArchivedLogDestId: NotRequired[int]
    AdditionalArchivedLogDestId: NotRequired[int]
    ExtraArchivedLogDestIds: NotRequired[List[int]]
    AllowSelectNestedTables: NotRequired[bool]
    ParallelAsmReadThreads: NotRequired[int]
    ReadAheadBlocks: NotRequired[int]
    AccessAlternateDirectly: NotRequired[bool]
    UseAlternateFolderForOnline: NotRequired[bool]
    OraclePathPrefix: NotRequired[str]
    UsePathPrefix: NotRequired[str]
    ReplacePathPrefix: NotRequired[bool]
    EnableHomogenousTablespace: NotRequired[bool]
    DirectPathNoLog: NotRequired[bool]
    ArchivedLogsOnly: NotRequired[bool]
    AsmPassword: NotRequired[str]
    AsmServer: NotRequired[str]
    AsmUser: NotRequired[str]
    CharLengthSemantics: NotRequired[CharLengthSemanticsType]
    DatabaseName: NotRequired[str]
    DirectPathParallelLoad: NotRequired[bool]
    FailTasksOnLobTruncation: NotRequired[bool]
    NumberDatatypeScale: NotRequired[int]
    Password: NotRequired[str]
    Port: NotRequired[int]
    ReadTableSpaceName: NotRequired[bool]
    RetryInterval: NotRequired[int]
    SecurityDbEncryption: NotRequired[str]
    SecurityDbEncryptionName: NotRequired[str]
    ServerName: NotRequired[str]
    SpatialDataOptionToGeoJsonFunctionName: NotRequired[str]
    StandbyDelayTime: NotRequired[int]
    Username: NotRequired[str]
    UseBFile: NotRequired[bool]
    UseDirectPathFullLoad: NotRequired[bool]
    UseLogminerReader: NotRequired[bool]
    SecretsManagerAccessRoleArn: NotRequired[str]
    SecretsManagerSecretId: NotRequired[str]
    SecretsManagerOracleAsmAccessRoleArn: NotRequired[str]
    SecretsManagerOracleAsmSecretId: NotRequired[str]
    TrimSpaceInChar: NotRequired[bool]
    ConvertTimestampWithZoneToUTC: NotRequired[bool]
    OpenTransactionWindow: NotRequired[int]
    AuthenticationMethod: NotRequired[OracleAuthenticationMethodType]


class ExportMetadataModelAssessmentMessageRequestTypeDef(TypedDict):
    MigrationProjectIdentifier: str
    SelectionRules: str
    FileName: NotRequired[str]
    AssessmentReportTypes: NotRequired[Sequence[AssessmentReportTypeType]]


class ExportMetadataModelAssessmentResultEntryTypeDef(TypedDict):
    S3ObjectKey: NotRequired[str]
    ObjectURL: NotRequired[str]


class ExportSqlDetailsTypeDef(TypedDict):
    S3ObjectKey: NotRequired[str]
    ObjectURL: NotRequired[str]


class ListTagsForResourceMessageRequestTypeDef(TypedDict):
    ResourceArn: NotRequired[str]
    ResourceArnList: NotRequired[Sequence[str]]


class ModifyConversionConfigurationMessageRequestTypeDef(TypedDict):
    MigrationProjectIdentifier: str
    ConversionConfiguration: str


class ModifyEventSubscriptionMessageRequestTypeDef(TypedDict):
    SubscriptionName: str
    SnsTopicArn: NotRequired[str]
    SourceType: NotRequired[str]
    EventCategories: NotRequired[Sequence[str]]
    Enabled: NotRequired[bool]


class ModifyInstanceProfileMessageRequestTypeDef(TypedDict):
    InstanceProfileIdentifier: str
    AvailabilityZone: NotRequired[str]
    KmsKeyArn: NotRequired[str]
    PubliclyAccessible: NotRequired[bool]
    NetworkType: NotRequired[str]
    InstanceProfileName: NotRequired[str]
    Description: NotRequired[str]
    SubnetGroupIdentifier: NotRequired[str]
    VpcSecurityGroups: NotRequired[Sequence[str]]


class ModifyReplicationSubnetGroupMessageRequestTypeDef(TypedDict):
    ReplicationSubnetGroupIdentifier: str
    SubnetIds: Sequence[str]
    ReplicationSubnetGroupDescription: NotRequired[str]


class MoveReplicationTaskMessageRequestTypeDef(TypedDict):
    ReplicationTaskArn: str
    TargetReplicationInstanceArn: str


class PendingMaintenanceActionTypeDef(TypedDict):
    Action: NotRequired[str]
    AutoAppliedAfterDate: NotRequired[datetime]
    ForcedApplyDate: NotRequired[datetime]
    OptInStatus: NotRequired[str]
    CurrentApplyDate: NotRequired[datetime]
    Description: NotRequired[str]


class ProvisionDataTypeDef(TypedDict):
    ProvisionState: NotRequired[str]
    ProvisionedCapacityUnits: NotRequired[int]
    DateProvisioned: NotRequired[datetime]
    IsNewProvisioningAvailable: NotRequired[bool]
    DateNewProvisioningDataAvailable: NotRequired[datetime]
    ReasonForNewProvisioningData: NotRequired[str]


class RdsConfigurationTypeDef(TypedDict):
    EngineEdition: NotRequired[str]
    InstanceType: NotRequired[str]
    InstanceVcpu: NotRequired[float]
    InstanceMemory: NotRequired[float]
    StorageType: NotRequired[str]
    StorageSize: NotRequired[int]
    StorageIops: NotRequired[int]
    DeploymentOption: NotRequired[str]
    EngineVersion: NotRequired[str]


class RdsRequirementsTypeDef(TypedDict):
    EngineEdition: NotRequired[str]
    InstanceVcpu: NotRequired[float]
    InstanceMemory: NotRequired[float]
    StorageSize: NotRequired[int]
    StorageIops: NotRequired[int]
    DeploymentOption: NotRequired[str]
    EngineVersion: NotRequired[str]


class RebootReplicationInstanceMessageRequestTypeDef(TypedDict):
    ReplicationInstanceArn: str
    ForceFailover: NotRequired[bool]
    ForcePlannedFailover: NotRequired[bool]


class RecommendationSettingsTypeDef(TypedDict):
    InstanceSizingType: str
    WorkloadType: str


class RefreshSchemasMessageRequestTypeDef(TypedDict):
    EndpointArn: str
    ReplicationInstanceArn: str


class TableToReloadTypeDef(TypedDict):
    SchemaName: str
    TableName: str


class RemoveTagsFromResourceMessageRequestTypeDef(TypedDict):
    ResourceArn: str
    TagKeys: Sequence[str]


class ReplicationPendingModifiedValuesTypeDef(TypedDict):
    ReplicationInstanceClass: NotRequired[str]
    AllocatedStorage: NotRequired[int]
    MultiAZ: NotRequired[bool]
    EngineVersion: NotRequired[str]
    NetworkType: NotRequired[str]


class VpcSecurityGroupMembershipTypeDef(TypedDict):
    VpcSecurityGroupId: NotRequired[str]
    Status: NotRequired[str]


class ReplicationStatsTypeDef(TypedDict):
    FullLoadProgressPercent: NotRequired[int]
    ElapsedTimeMillis: NotRequired[int]
    TablesLoaded: NotRequired[int]
    TablesLoading: NotRequired[int]
    TablesQueued: NotRequired[int]
    TablesErrored: NotRequired[int]
    FreshStartDate: NotRequired[datetime]
    StartDate: NotRequired[datetime]
    StopDate: NotRequired[datetime]
    FullLoadStartDate: NotRequired[datetime]
    FullLoadFinishDate: NotRequired[datetime]


class ReplicationTaskAssessmentRunProgressTypeDef(TypedDict):
    IndividualAssessmentCount: NotRequired[int]
    IndividualAssessmentCompletedCount: NotRequired[int]


ReplicationTaskAssessmentRunResultStatisticTypeDef = TypedDict(
    "ReplicationTaskAssessmentRunResultStatisticTypeDef",
    {
        "Passed": NotRequired[int],
        "Failed": NotRequired[int],
        "Error": NotRequired[int],
        "Warning": NotRequired[int],
        "Cancelled": NotRequired[int],
    },
)


class ReplicationTaskStatsTypeDef(TypedDict):
    FullLoadProgressPercent: NotRequired[int]
    ElapsedTimeMillis: NotRequired[int]
    TablesLoaded: NotRequired[int]
    TablesLoading: NotRequired[int]
    TablesQueued: NotRequired[int]
    TablesErrored: NotRequired[int]
    FreshStartDate: NotRequired[datetime]
    StartDate: NotRequired[datetime]
    StopDate: NotRequired[datetime]
    FullLoadStartDate: NotRequired[datetime]
    FullLoadFinishDate: NotRequired[datetime]


class SchemaShortInfoResponseTypeDef(TypedDict):
    SchemaId: NotRequired[str]
    SchemaName: NotRequired[str]
    DatabaseId: NotRequired[str]
    DatabaseName: NotRequired[str]
    DatabaseIpAddress: NotRequired[str]


class StartDataMigrationMessageRequestTypeDef(TypedDict):
    DataMigrationIdentifier: str
    StartType: StartReplicationMigrationTypeValueType


class StartExtensionPackAssociationMessageRequestTypeDef(TypedDict):
    MigrationProjectIdentifier: str


class StartMetadataModelAssessmentMessageRequestTypeDef(TypedDict):
    MigrationProjectIdentifier: str
    SelectionRules: str


class StartMetadataModelConversionMessageRequestTypeDef(TypedDict):
    MigrationProjectIdentifier: str
    SelectionRules: str


class StartMetadataModelExportAsScriptMessageRequestTypeDef(TypedDict):
    MigrationProjectIdentifier: str
    SelectionRules: str
    Origin: OriginTypeValueType
    FileName: NotRequired[str]


class StartMetadataModelExportToTargetMessageRequestTypeDef(TypedDict):
    MigrationProjectIdentifier: str
    SelectionRules: str
    OverwriteExtensionPack: NotRequired[bool]


class StartMetadataModelImportMessageRequestTypeDef(TypedDict):
    MigrationProjectIdentifier: str
    SelectionRules: str
    Origin: OriginTypeValueType
    Refresh: NotRequired[bool]


class StartReplicationTaskAssessmentMessageRequestTypeDef(TypedDict):
    ReplicationTaskArn: str


class StopDataMigrationMessageRequestTypeDef(TypedDict):
    DataMigrationIdentifier: str


class StopReplicationMessageRequestTypeDef(TypedDict):
    ReplicationConfigArn: str


class StopReplicationTaskMessageRequestTypeDef(TypedDict):
    ReplicationTaskArn: str


class TestConnectionMessageRequestTypeDef(TypedDict):
    ReplicationInstanceArn: str
    EndpointArn: str


class UpdateSubscriptionsToEventBridgeMessageRequestTypeDef(TypedDict):
    ForceMove: NotRequired[bool]


class AddTagsToResourceMessageRequestTypeDef(TypedDict):
    ResourceArn: str
    Tags: Sequence[TagTypeDef]


class CreateEventSubscriptionMessageRequestTypeDef(TypedDict):
    SubscriptionName: str
    SnsTopicArn: str
    SourceType: NotRequired[str]
    EventCategories: NotRequired[Sequence[str]]
    SourceIds: NotRequired[Sequence[str]]
    Enabled: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateInstanceProfileMessageRequestTypeDef(TypedDict):
    AvailabilityZone: NotRequired[str]
    KmsKeyArn: NotRequired[str]
    PubliclyAccessible: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]
    NetworkType: NotRequired[str]
    InstanceProfileName: NotRequired[str]
    Description: NotRequired[str]
    SubnetGroupIdentifier: NotRequired[str]
    VpcSecurityGroups: NotRequired[Sequence[str]]


class CreateReplicationSubnetGroupMessageRequestTypeDef(TypedDict):
    ReplicationSubnetGroupIdentifier: str
    ReplicationSubnetGroupDescription: str
    SubnetIds: Sequence[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class StartReplicationTaskAssessmentRunMessageRequestTypeDef(TypedDict):
    ReplicationTaskArn: str
    ServiceAccessRoleArn: str
    ResultLocationBucket: str
    AssessmentRunName: str
    ResultLocationFolder: NotRequired[str]
    ResultEncryptionMode: NotRequired[str]
    ResultKmsKeyArn: NotRequired[str]
    IncludeOnly: NotRequired[Sequence[str]]
    Exclude: NotRequired[Sequence[str]]
    Tags: NotRequired[Sequence[TagTypeDef]]


class CreateFleetAdvisorCollectorResponseTypeDef(TypedDict):
    CollectorReferencedId: str
    CollectorName: str
    Description: str
    ServiceAccessRoleArn: str
    S3BucketName: str
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteFleetAdvisorDatabasesResponseTypeDef(TypedDict):
    DatabaseIds: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeAccountAttributesResponseTypeDef(TypedDict):
    AccountQuotas: List[AccountQuotaTypeDef]
    UniqueAccountIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeApplicableIndividualAssessmentsResponseTypeDef(TypedDict):
    IndividualAssessmentNames: List[str]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeConversionConfigurationResponseTypeDef(TypedDict):
    MigrationProjectIdentifier: str
    ConversionConfiguration: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeSchemasResponseTypeDef(TypedDict):
    Marker: str
    Schemas: List[str]
    ResponseMetadata: ResponseMetadataTypeDef


class EmptyResponseMetadataTypeDef(TypedDict):
    ResponseMetadata: ResponseMetadataTypeDef


class ListTagsForResourceResponseTypeDef(TypedDict):
    TagList: List[TagTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyConversionConfigurationResponseTypeDef(TypedDict):
    MigrationProjectIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef


class ReloadReplicationTablesResponseTypeDef(TypedDict):
    ReplicationConfigArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class ReloadTablesResponseTypeDef(TypedDict):
    ReplicationTaskArn: str
    ResponseMetadata: ResponseMetadataTypeDef


class RunFleetAdvisorLsaAnalysisResponseTypeDef(TypedDict):
    LsaAnalysisId: str
    Status: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartExtensionPackAssociationResponseTypeDef(TypedDict):
    RequestIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartMetadataModelAssessmentResponseTypeDef(TypedDict):
    RequestIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartMetadataModelConversionResponseTypeDef(TypedDict):
    RequestIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartMetadataModelExportAsScriptResponseTypeDef(TypedDict):
    RequestIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartMetadataModelExportToTargetResponseTypeDef(TypedDict):
    RequestIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef


class StartMetadataModelImportResponseTypeDef(TypedDict):
    RequestIdentifier: str
    ResponseMetadata: ResponseMetadataTypeDef


class UpdateSubscriptionsToEventBridgeResponseTypeDef(TypedDict):
    Result: str
    ResponseMetadata: ResponseMetadataTypeDef


class SubnetTypeDef(TypedDict):
    SubnetIdentifier: NotRequired[str]
    SubnetAvailabilityZone: NotRequired[AvailabilityZoneTypeDef]
    SubnetStatus: NotRequired[str]


class BatchStartRecommendationsResponseTypeDef(TypedDict):
    ErrorEntries: List[BatchStartRecommendationsErrorEntryTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ImportCertificateMessageRequestTypeDef(TypedDict):
    CertificateIdentifier: str
    CertificatePem: NotRequired[str]
    CertificateWallet: NotRequired[BlobTypeDef]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DeleteCertificateResponseTypeDef(TypedDict):
    Certificate: CertificateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeCertificatesResponseTypeDef(TypedDict):
    Marker: str
    Certificates: List[CertificateTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ImportCertificateResponseTypeDef(TypedDict):
    Certificate: CertificateTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CollectorResponseTypeDef(TypedDict):
    CollectorReferencedId: NotRequired[str]
    CollectorName: NotRequired[str]
    CollectorVersion: NotRequired[str]
    VersionStatus: NotRequired[VersionStatusType]
    Description: NotRequired[str]
    S3BucketName: NotRequired[str]
    ServiceAccessRoleArn: NotRequired[str]
    CollectorHealthCheck: NotRequired[CollectorHealthCheckTypeDef]
    LastDataReceived: NotRequired[str]
    RegisteredDate: NotRequired[str]
    CreatedDate: NotRequired[str]
    ModifiedDate: NotRequired[str]
    InventoryData: NotRequired[InventoryDataTypeDef]


class ReplicationConfigTypeDef(TypedDict):
    ReplicationConfigIdentifier: NotRequired[str]
    ReplicationConfigArn: NotRequired[str]
    SourceEndpointArn: NotRequired[str]
    TargetEndpointArn: NotRequired[str]
    ReplicationType: NotRequired[MigrationTypeValueType]
    ComputeConfig: NotRequired[ComputeConfigOutputTypeDef]
    ReplicationSettings: NotRequired[str]
    SupplementalSettings: NotRequired[str]
    TableMappings: NotRequired[str]
    ReplicationConfigCreateTime: NotRequired[datetime]
    ReplicationConfigUpdateTime: NotRequired[datetime]


class CreateReplicationConfigMessageRequestTypeDef(TypedDict):
    ReplicationConfigIdentifier: str
    SourceEndpointArn: str
    TargetEndpointArn: str
    ComputeConfig: ComputeConfigTypeDef
    ReplicationType: MigrationTypeValueType
    TableMappings: str
    ReplicationSettings: NotRequired[str]
    SupplementalSettings: NotRequired[str]
    ResourceIdentifier: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class ModifyReplicationConfigMessageRequestTypeDef(TypedDict):
    ReplicationConfigArn: str
    ReplicationConfigIdentifier: NotRequired[str]
    ReplicationType: NotRequired[MigrationTypeValueType]
    TableMappings: NotRequired[str]
    ReplicationSettings: NotRequired[str]
    SupplementalSettings: NotRequired[str]
    ComputeConfig: NotRequired[ComputeConfigTypeDef]
    SourceEndpointArn: NotRequired[str]
    TargetEndpointArn: NotRequired[str]


class DeleteConnectionResponseTypeDef(TypedDict):
    Connection: ConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeConnectionsResponseTypeDef(TypedDict):
    Marker: str
    Connections: List[ConnectionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class TestConnectionResponseTypeDef(TypedDict):
    Connection: ConnectionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateEndpointMessageRequestTypeDef(TypedDict):
    EndpointIdentifier: str
    EndpointType: ReplicationEndpointTypeValueType
    EngineName: str
    Username: NotRequired[str]
    Password: NotRequired[str]
    ServerName: NotRequired[str]
    Port: NotRequired[int]
    DatabaseName: NotRequired[str]
    ExtraConnectionAttributes: NotRequired[str]
    KmsKeyId: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    CertificateArn: NotRequired[str]
    SslMode: NotRequired[DmsSslModeValueType]
    ServiceAccessRoleArn: NotRequired[str]
    ExternalTableDefinition: NotRequired[str]
    DynamoDbSettings: NotRequired[DynamoDbSettingsTypeDef]
    S3Settings: NotRequired[S3SettingsTypeDef]
    DmsTransferSettings: NotRequired[DmsTransferSettingsTypeDef]
    MongoDbSettings: NotRequired[MongoDbSettingsTypeDef]
    KinesisSettings: NotRequired[KinesisSettingsTypeDef]
    KafkaSettings: NotRequired[KafkaSettingsTypeDef]
    ElasticsearchSettings: NotRequired[ElasticsearchSettingsTypeDef]
    NeptuneSettings: NotRequired[NeptuneSettingsTypeDef]
    RedshiftSettings: NotRequired[RedshiftSettingsTypeDef]
    PostgreSQLSettings: NotRequired[PostgreSQLSettingsTypeDef]
    MySQLSettings: NotRequired[MySQLSettingsTypeDef]
    OracleSettings: NotRequired[OracleSettingsTypeDef]
    SybaseSettings: NotRequired[SybaseSettingsTypeDef]
    MicrosoftSQLServerSettings: NotRequired[MicrosoftSQLServerSettingsTypeDef]
    IBMDb2Settings: NotRequired[IBMDb2SettingsTypeDef]
    ResourceIdentifier: NotRequired[str]
    DocDbSettings: NotRequired[DocDbSettingsTypeDef]
    RedisSettings: NotRequired[RedisSettingsTypeDef]
    GcpMySQLSettings: NotRequired[GcpMySQLSettingsTypeDef]
    TimestreamSettings: NotRequired[TimestreamSettingsTypeDef]


class ModifyEndpointMessageRequestTypeDef(TypedDict):
    EndpointArn: str
    EndpointIdentifier: NotRequired[str]
    EndpointType: NotRequired[ReplicationEndpointTypeValueType]
    EngineName: NotRequired[str]
    Username: NotRequired[str]
    Password: NotRequired[str]
    ServerName: NotRequired[str]
    Port: NotRequired[int]
    DatabaseName: NotRequired[str]
    ExtraConnectionAttributes: NotRequired[str]
    CertificateArn: NotRequired[str]
    SslMode: NotRequired[DmsSslModeValueType]
    ServiceAccessRoleArn: NotRequired[str]
    ExternalTableDefinition: NotRequired[str]
    DynamoDbSettings: NotRequired[DynamoDbSettingsTypeDef]
    S3Settings: NotRequired[S3SettingsTypeDef]
    DmsTransferSettings: NotRequired[DmsTransferSettingsTypeDef]
    MongoDbSettings: NotRequired[MongoDbSettingsTypeDef]
    KinesisSettings: NotRequired[KinesisSettingsTypeDef]
    KafkaSettings: NotRequired[KafkaSettingsTypeDef]
    ElasticsearchSettings: NotRequired[ElasticsearchSettingsTypeDef]
    NeptuneSettings: NotRequired[NeptuneSettingsTypeDef]
    RedshiftSettings: NotRequired[RedshiftSettingsTypeDef]
    PostgreSQLSettings: NotRequired[PostgreSQLSettingsTypeDef]
    MySQLSettings: NotRequired[MySQLSettingsTypeDef]
    OracleSettings: NotRequired[OracleSettingsTypeDef]
    SybaseSettings: NotRequired[SybaseSettingsTypeDef]
    MicrosoftSQLServerSettings: NotRequired[MicrosoftSQLServerSettingsTypeDef]
    IBMDb2Settings: NotRequired[IBMDb2SettingsTypeDef]
    DocDbSettings: NotRequired[DocDbSettingsTypeDef]
    RedisSettings: NotRequired[RedisSettingsTypeDef]
    ExactSettings: NotRequired[bool]
    GcpMySQLSettings: NotRequired[GcpMySQLSettingsTypeDef]
    TimestreamSettings: NotRequired[TimestreamSettingsTypeDef]


class CreateEventSubscriptionResponseTypeDef(TypedDict):
    EventSubscription: EventSubscriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteEventSubscriptionResponseTypeDef(TypedDict):
    EventSubscription: EventSubscriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEventSubscriptionsResponseTypeDef(TypedDict):
    Marker: str
    EventSubscriptionsList: List[EventSubscriptionTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyEventSubscriptionResponseTypeDef(TypedDict):
    EventSubscription: EventSubscriptionTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateInstanceProfileResponseTypeDef(TypedDict):
    InstanceProfile: InstanceProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteInstanceProfileResponseTypeDef(TypedDict):
    InstanceProfile: InstanceProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeInstanceProfilesResponseTypeDef(TypedDict):
    Marker: str
    InstanceProfiles: List[InstanceProfileTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyInstanceProfileResponseTypeDef(TypedDict):
    InstanceProfile: InstanceProfileTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMigrationProjectMessageRequestTypeDef(TypedDict):
    SourceDataProviderDescriptors: Sequence[DataProviderDescriptorDefinitionTypeDef]
    TargetDataProviderDescriptors: Sequence[DataProviderDescriptorDefinitionTypeDef]
    InstanceProfileIdentifier: str
    MigrationProjectName: NotRequired[str]
    TransformationRules: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    SchemaConversionApplicationAttributes: NotRequired[SCApplicationAttributesTypeDef]


class ModifyMigrationProjectMessageRequestTypeDef(TypedDict):
    MigrationProjectIdentifier: str
    MigrationProjectName: NotRequired[str]
    SourceDataProviderDescriptors: NotRequired[Sequence[DataProviderDescriptorDefinitionTypeDef]]
    TargetDataProviderDescriptors: NotRequired[Sequence[DataProviderDescriptorDefinitionTypeDef]]
    InstanceProfileIdentifier: NotRequired[str]
    TransformationRules: NotRequired[str]
    Description: NotRequired[str]
    SchemaConversionApplicationAttributes: NotRequired[SCApplicationAttributesTypeDef]


class CreateReplicationInstanceMessageRequestTypeDef(TypedDict):
    ReplicationInstanceIdentifier: str
    ReplicationInstanceClass: str
    AllocatedStorage: NotRequired[int]
    VpcSecurityGroupIds: NotRequired[Sequence[str]]
    AvailabilityZone: NotRequired[str]
    ReplicationSubnetGroupIdentifier: NotRequired[str]
    PreferredMaintenanceWindow: NotRequired[str]
    MultiAZ: NotRequired[bool]
    EngineVersion: NotRequired[str]
    AutoMinorVersionUpgrade: NotRequired[bool]
    Tags: NotRequired[Sequence[TagTypeDef]]
    KmsKeyId: NotRequired[str]
    PubliclyAccessible: NotRequired[bool]
    DnsNameServers: NotRequired[str]
    ResourceIdentifier: NotRequired[str]
    NetworkType: NotRequired[str]
    KerberosAuthenticationSettings: NotRequired[KerberosAuthenticationSettingsTypeDef]


class ModifyReplicationInstanceMessageRequestTypeDef(TypedDict):
    ReplicationInstanceArn: str
    AllocatedStorage: NotRequired[int]
    ApplyImmediately: NotRequired[bool]
    ReplicationInstanceClass: NotRequired[str]
    VpcSecurityGroupIds: NotRequired[Sequence[str]]
    PreferredMaintenanceWindow: NotRequired[str]
    MultiAZ: NotRequired[bool]
    EngineVersion: NotRequired[str]
    AllowMajorVersionUpgrade: NotRequired[bool]
    AutoMinorVersionUpgrade: NotRequired[bool]
    ReplicationInstanceIdentifier: NotRequired[str]
    NetworkType: NotRequired[str]
    KerberosAuthenticationSettings: NotRequired[KerberosAuthenticationSettingsTypeDef]


class CreateReplicationTaskMessageRequestTypeDef(TypedDict):
    ReplicationTaskIdentifier: str
    SourceEndpointArn: str
    TargetEndpointArn: str
    ReplicationInstanceArn: str
    MigrationType: MigrationTypeValueType
    TableMappings: str
    ReplicationTaskSettings: NotRequired[str]
    CdcStartTime: NotRequired[TimestampTypeDef]
    CdcStartPosition: NotRequired[str]
    CdcStopPosition: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]
    TaskData: NotRequired[str]
    ResourceIdentifier: NotRequired[str]


class ModifyReplicationTaskMessageRequestTypeDef(TypedDict):
    ReplicationTaskArn: str
    ReplicationTaskIdentifier: NotRequired[str]
    MigrationType: NotRequired[MigrationTypeValueType]
    TableMappings: NotRequired[str]
    ReplicationTaskSettings: NotRequired[str]
    CdcStartTime: NotRequired[TimestampTypeDef]
    CdcStartPosition: NotRequired[str]
    CdcStopPosition: NotRequired[str]
    TaskData: NotRequired[str]


class SourceDataSettingTypeDef(TypedDict):
    CDCStartPosition: NotRequired[str]
    CDCStartTime: NotRequired[TimestampTypeDef]
    CDCStopTime: NotRequired[TimestampTypeDef]
    SlotName: NotRequired[str]


class StartReplicationMessageRequestTypeDef(TypedDict):
    ReplicationConfigArn: str
    StartReplicationType: str
    CdcStartTime: NotRequired[TimestampTypeDef]
    CdcStartPosition: NotRequired[str]
    CdcStopPosition: NotRequired[str]


class StartReplicationTaskMessageRequestTypeDef(TypedDict):
    ReplicationTaskArn: str
    StartReplicationTaskType: StartReplicationTaskTypeValueType
    CdcStartTime: NotRequired[TimestampTypeDef]
    CdcStartPosition: NotRequired[str]
    CdcStopPosition: NotRequired[str]


class DataMigrationTypeDef(TypedDict):
    DataMigrationName: NotRequired[str]
    DataMigrationArn: NotRequired[str]
    DataMigrationCreateTime: NotRequired[datetime]
    DataMigrationStartTime: NotRequired[datetime]
    DataMigrationEndTime: NotRequired[datetime]
    ServiceAccessRoleArn: NotRequired[str]
    MigrationProjectArn: NotRequired[str]
    DataMigrationType: NotRequired[MigrationTypeValueType]
    DataMigrationSettings: NotRequired[DataMigrationSettingsTypeDef]
    SourceDataSettings: NotRequired[List[SourceDataSettingOutputTypeDef]]
    DataMigrationStatistics: NotRequired[DataMigrationStatisticsTypeDef]
    DataMigrationStatus: NotRequired[str]
    PublicIpAddresses: NotRequired[List[str]]
    DataMigrationCidrBlocks: NotRequired[List[str]]
    LastFailureMessage: NotRequired[str]
    StopReason: NotRequired[str]


class MigrationProjectTypeDef(TypedDict):
    MigrationProjectName: NotRequired[str]
    MigrationProjectArn: NotRequired[str]
    MigrationProjectCreationTime: NotRequired[datetime]
    SourceDataProviderDescriptors: NotRequired[List[DataProviderDescriptorTypeDef]]
    TargetDataProviderDescriptors: NotRequired[List[DataProviderDescriptorTypeDef]]
    InstanceProfileArn: NotRequired[str]
    InstanceProfileName: NotRequired[str]
    TransformationRules: NotRequired[str]
    Description: NotRequired[str]
    SchemaConversionApplicationAttributes: NotRequired[SCApplicationAttributesTypeDef]


class DataProviderSettingsTypeDef(TypedDict):
    RedshiftSettings: NotRequired[RedshiftDataProviderSettingsTypeDef]
    PostgreSqlSettings: NotRequired[PostgreSqlDataProviderSettingsTypeDef]
    MySqlSettings: NotRequired[MySqlDataProviderSettingsTypeDef]
    OracleSettings: NotRequired[OracleDataProviderSettingsTypeDef]
    MicrosoftSqlServerSettings: NotRequired[MicrosoftSqlServerDataProviderSettingsTypeDef]
    DocDbSettings: NotRequired[DocDbDataProviderSettingsTypeDef]
    MariaDbSettings: NotRequired[MariaDbDataProviderSettingsTypeDef]
    MongoDbSettings: NotRequired[MongoDbDataProviderSettingsTypeDef]


class DatabaseResponseTypeDef(TypedDict):
    DatabaseId: NotRequired[str]
    DatabaseName: NotRequired[str]
    IpAddress: NotRequired[str]
    NumberOfSchemas: NotRequired[int]
    Server: NotRequired[ServerShortInfoResponseTypeDef]
    SoftwareDetails: NotRequired[DatabaseInstanceSoftwareDetailsResponseTypeDef]
    Collectors: NotRequired[List[CollectorShortInfoResponseTypeDef]]


class ErrorDetailsTypeDef(TypedDict):
    defaultErrorDetails: NotRequired[DefaultErrorDetailsTypeDef]


class DescribeCertificatesMessageRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeConnectionsMessageRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeDataMigrationsMessageRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    WithoutSettings: NotRequired[bool]
    WithoutStatistics: NotRequired[bool]


class DescribeDataProvidersMessageRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeEndpointTypesMessageRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeEndpointsMessageRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeEventCategoriesMessageRequestTypeDef(TypedDict):
    SourceType: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeEventSubscriptionsMessageRequestTypeDef(TypedDict):
    SubscriptionName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeEventsMessageRequestTypeDef(TypedDict):
    SourceIdentifier: NotRequired[str]
    SourceType: NotRequired[Literal["replication-instance"]]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Duration: NotRequired[int]
    EventCategories: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeExtensionPackAssociationsMessageRequestTypeDef(TypedDict):
    MigrationProjectIdentifier: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]


class DescribeFleetAdvisorCollectorsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeFleetAdvisorDatabasesRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeFleetAdvisorSchemaObjectSummaryRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeFleetAdvisorSchemasRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeInstanceProfilesMessageRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeMetadataModelAssessmentsMessageRequestTypeDef(TypedDict):
    MigrationProjectIdentifier: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]


class DescribeMetadataModelConversionsMessageRequestTypeDef(TypedDict):
    MigrationProjectIdentifier: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]


class DescribeMetadataModelExportsAsScriptMessageRequestTypeDef(TypedDict):
    MigrationProjectIdentifier: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]


class DescribeMetadataModelExportsToTargetMessageRequestTypeDef(TypedDict):
    MigrationProjectIdentifier: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]


class DescribeMetadataModelImportsMessageRequestTypeDef(TypedDict):
    MigrationProjectIdentifier: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]


class DescribeMigrationProjectsMessageRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribePendingMaintenanceActionsMessageRequestTypeDef(TypedDict):
    ReplicationInstanceArn: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    Marker: NotRequired[str]
    MaxRecords: NotRequired[int]


class DescribeRecommendationLimitationsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeRecommendationsRequestRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    NextToken: NotRequired[str]


class DescribeReplicationConfigsMessageRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeReplicationInstancesMessageRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeReplicationSubnetGroupsMessageRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeReplicationTableStatisticsMessageRequestTypeDef(TypedDict):
    ReplicationConfigArn: str
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeReplicationTaskAssessmentRunsMessageRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeReplicationTaskIndividualAssessmentsMessageRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeReplicationTasksMessageRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    WithoutSettings: NotRequired[bool]


class DescribeReplicationsMessageRequestTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]


class DescribeTableStatisticsMessageRequestTypeDef(TypedDict):
    ReplicationTaskArn: str
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]


class DescribeCertificatesMessagePaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeConnectionsMessagePaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeDataMigrationsMessagePaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    WithoutSettings: NotRequired[bool]
    WithoutStatistics: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeEndpointTypesMessagePaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeEndpointsMessagePaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeEventSubscriptionsMessagePaginateTypeDef(TypedDict):
    SubscriptionName: NotRequired[str]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeEventsMessagePaginateTypeDef(TypedDict):
    SourceIdentifier: NotRequired[str]
    SourceType: NotRequired[Literal["replication-instance"]]
    StartTime: NotRequired[TimestampTypeDef]
    EndTime: NotRequired[TimestampTypeDef]
    Duration: NotRequired[int]
    EventCategories: NotRequired[Sequence[str]]
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeOrderableReplicationInstancesMessagePaginateTypeDef(TypedDict):
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeReplicationInstancesMessagePaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeReplicationSubnetGroupsMessagePaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeReplicationTaskAssessmentResultsMessagePaginateTypeDef(TypedDict):
    ReplicationTaskArn: NotRequired[str]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeReplicationTasksMessagePaginateTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    WithoutSettings: NotRequired[bool]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeSchemasMessagePaginateTypeDef(TypedDict):
    EndpointArn: str
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeTableStatisticsMessagePaginateTypeDef(TypedDict):
    ReplicationTaskArn: str
    Filters: NotRequired[Sequence[FilterTypeDef]]
    PaginationConfig: NotRequired[PaginatorConfigTypeDef]


class DescribeConnectionsMessageWaitTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeEndpointsMessageWaitTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeReplicationInstancesMessageWaitTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeReplicationTasksMessageWaitTypeDef(TypedDict):
    Filters: NotRequired[Sequence[FilterTypeDef]]
    MaxRecords: NotRequired[int]
    Marker: NotRequired[str]
    WithoutSettings: NotRequired[bool]
    WaiterConfig: NotRequired[WaiterConfigTypeDef]


class DescribeEndpointSettingsResponseTypeDef(TypedDict):
    Marker: str
    EndpointSettings: List[EndpointSettingTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEndpointTypesResponseTypeDef(TypedDict):
    Marker: str
    SupportedEndpointTypes: List[SupportedEndpointTypeTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEngineVersionsResponseTypeDef(TypedDict):
    EngineVersions: List[EngineVersionTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEventCategoriesResponseTypeDef(TypedDict):
    EventCategoryGroupList: List[EventCategoryGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEventsResponseTypeDef(TypedDict):
    Marker: str
    Events: List[EventTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFleetAdvisorLsaAnalysisResponseTypeDef(TypedDict):
    Analysis: List[FleetAdvisorLsaAnalysisResponseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeFleetAdvisorSchemaObjectSummaryResponseTypeDef(TypedDict):
    FleetAdvisorSchemaObjects: List[FleetAdvisorSchemaObjectResponseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeOrderableReplicationInstancesResponseTypeDef(TypedDict):
    OrderableReplicationInstances: List[OrderableReplicationInstanceTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeRecommendationLimitationsResponseTypeDef(TypedDict):
    Limitations: List[LimitationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class DescribeRefreshSchemasStatusResponseTypeDef(TypedDict):
    RefreshSchemasStatus: RefreshSchemasStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RefreshSchemasResponseTypeDef(TypedDict):
    RefreshSchemasStatus: RefreshSchemasStatusTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeReplicationInstanceTaskLogsResponseTypeDef(TypedDict):
    ReplicationInstanceArn: str
    ReplicationInstanceTaskLogs: List[ReplicationInstanceTaskLogTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeReplicationTableStatisticsResponseTypeDef(TypedDict):
    ReplicationConfigArn: str
    Marker: str
    ReplicationTableStatistics: List[TableStatisticsTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeTableStatisticsResponseTypeDef(TypedDict):
    ReplicationTaskArn: str
    TableStatistics: List[TableStatisticsTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeReplicationTaskAssessmentResultsResponseTypeDef(TypedDict):
    Marker: str
    BucketName: str
    ReplicationTaskAssessmentResults: List[ReplicationTaskAssessmentResultTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeReplicationTaskIndividualAssessmentsResponseTypeDef(TypedDict):
    Marker: str
    ReplicationTaskIndividualAssessments: List[ReplicationTaskIndividualAssessmentTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class EndpointTypeDef(TypedDict):
    EndpointIdentifier: NotRequired[str]
    EndpointType: NotRequired[ReplicationEndpointTypeValueType]
    EngineName: NotRequired[str]
    EngineDisplayName: NotRequired[str]
    Username: NotRequired[str]
    ServerName: NotRequired[str]
    Port: NotRequired[int]
    DatabaseName: NotRequired[str]
    ExtraConnectionAttributes: NotRequired[str]
    Status: NotRequired[str]
    KmsKeyId: NotRequired[str]
    EndpointArn: NotRequired[str]
    CertificateArn: NotRequired[str]
    SslMode: NotRequired[DmsSslModeValueType]
    ServiceAccessRoleArn: NotRequired[str]
    ExternalTableDefinition: NotRequired[str]
    ExternalId: NotRequired[str]
    DynamoDbSettings: NotRequired[DynamoDbSettingsTypeDef]
    S3Settings: NotRequired[S3SettingsTypeDef]
    DmsTransferSettings: NotRequired[DmsTransferSettingsTypeDef]
    MongoDbSettings: NotRequired[MongoDbSettingsTypeDef]
    KinesisSettings: NotRequired[KinesisSettingsTypeDef]
    KafkaSettings: NotRequired[KafkaSettingsTypeDef]
    ElasticsearchSettings: NotRequired[ElasticsearchSettingsTypeDef]
    NeptuneSettings: NotRequired[NeptuneSettingsTypeDef]
    RedshiftSettings: NotRequired[RedshiftSettingsTypeDef]
    PostgreSQLSettings: NotRequired[PostgreSQLSettingsTypeDef]
    MySQLSettings: NotRequired[MySQLSettingsTypeDef]
    OracleSettings: NotRequired[OracleSettingsOutputTypeDef]
    SybaseSettings: NotRequired[SybaseSettingsTypeDef]
    MicrosoftSQLServerSettings: NotRequired[MicrosoftSQLServerSettingsTypeDef]
    IBMDb2Settings: NotRequired[IBMDb2SettingsTypeDef]
    DocDbSettings: NotRequired[DocDbSettingsTypeDef]
    RedisSettings: NotRequired[RedisSettingsTypeDef]
    GcpMySQLSettings: NotRequired[GcpMySQLSettingsTypeDef]
    TimestreamSettings: NotRequired[TimestreamSettingsTypeDef]


class ExportMetadataModelAssessmentResponseTypeDef(TypedDict):
    PdfReport: ExportMetadataModelAssessmentResultEntryTypeDef
    CsvReport: ExportMetadataModelAssessmentResultEntryTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ResourcePendingMaintenanceActionsTypeDef(TypedDict):
    ResourceIdentifier: NotRequired[str]
    PendingMaintenanceActionDetails: NotRequired[List[PendingMaintenanceActionTypeDef]]


class RdsRecommendationTypeDef(TypedDict):
    RequirementsToTarget: NotRequired[RdsRequirementsTypeDef]
    TargetConfiguration: NotRequired[RdsConfigurationTypeDef]


class StartRecommendationsRequestEntryTypeDef(TypedDict):
    DatabaseId: str
    Settings: RecommendationSettingsTypeDef


class StartRecommendationsRequestRequestTypeDef(TypedDict):
    DatabaseId: str
    Settings: RecommendationSettingsTypeDef


class ReloadReplicationTablesMessageRequestTypeDef(TypedDict):
    ReplicationConfigArn: str
    TablesToReload: Sequence[TableToReloadTypeDef]
    ReloadOption: NotRequired[ReloadOptionValueType]


class ReloadTablesMessageRequestTypeDef(TypedDict):
    ReplicationTaskArn: str
    TablesToReload: Sequence[TableToReloadTypeDef]
    ReloadOption: NotRequired[ReloadOptionValueType]


class ReplicationTypeDef(TypedDict):
    ReplicationConfigIdentifier: NotRequired[str]
    ReplicationConfigArn: NotRequired[str]
    SourceEndpointArn: NotRequired[str]
    TargetEndpointArn: NotRequired[str]
    ReplicationType: NotRequired[MigrationTypeValueType]
    Status: NotRequired[str]
    ProvisionData: NotRequired[ProvisionDataTypeDef]
    StopReason: NotRequired[str]
    FailureMessages: NotRequired[List[str]]
    ReplicationStats: NotRequired[ReplicationStatsTypeDef]
    StartReplicationType: NotRequired[str]
    CdcStartTime: NotRequired[datetime]
    CdcStartPosition: NotRequired[str]
    CdcStopPosition: NotRequired[str]
    RecoveryCheckpoint: NotRequired[str]
    ReplicationCreateTime: NotRequired[datetime]
    ReplicationUpdateTime: NotRequired[datetime]
    ReplicationLastStopTime: NotRequired[datetime]
    ReplicationDeprovisionTime: NotRequired[datetime]


class ReplicationTaskAssessmentRunTypeDef(TypedDict):
    ReplicationTaskAssessmentRunArn: NotRequired[str]
    ReplicationTaskArn: NotRequired[str]
    Status: NotRequired[str]
    ReplicationTaskAssessmentRunCreationDate: NotRequired[datetime]
    AssessmentProgress: NotRequired[ReplicationTaskAssessmentRunProgressTypeDef]
    LastFailureMessage: NotRequired[str]
    ServiceAccessRoleArn: NotRequired[str]
    ResultLocationBucket: NotRequired[str]
    ResultLocationFolder: NotRequired[str]
    ResultEncryptionMode: NotRequired[str]
    ResultKmsKeyArn: NotRequired[str]
    AssessmentRunName: NotRequired[str]
    IsLatestTaskAssessmentRun: NotRequired[bool]
    ResultStatistic: NotRequired[ReplicationTaskAssessmentRunResultStatisticTypeDef]


class ReplicationTaskTypeDef(TypedDict):
    ReplicationTaskIdentifier: NotRequired[str]
    SourceEndpointArn: NotRequired[str]
    TargetEndpointArn: NotRequired[str]
    ReplicationInstanceArn: NotRequired[str]
    MigrationType: NotRequired[MigrationTypeValueType]
    TableMappings: NotRequired[str]
    ReplicationTaskSettings: NotRequired[str]
    Status: NotRequired[str]
    LastFailureMessage: NotRequired[str]
    StopReason: NotRequired[str]
    ReplicationTaskCreationDate: NotRequired[datetime]
    ReplicationTaskStartDate: NotRequired[datetime]
    CdcStartPosition: NotRequired[str]
    CdcStopPosition: NotRequired[str]
    RecoveryCheckpoint: NotRequired[str]
    ReplicationTaskArn: NotRequired[str]
    ReplicationTaskStats: NotRequired[ReplicationTaskStatsTypeDef]
    TaskData: NotRequired[str]
    TargetReplicationInstanceArn: NotRequired[str]


class SchemaResponseTypeDef(TypedDict):
    CodeLineCount: NotRequired[int]
    CodeSize: NotRequired[int]
    Complexity: NotRequired[str]
    Server: NotRequired[ServerShortInfoResponseTypeDef]
    DatabaseInstance: NotRequired[DatabaseShortInfoResponseTypeDef]
    SchemaId: NotRequired[str]
    SchemaName: NotRequired[str]
    OriginalSchema: NotRequired[SchemaShortInfoResponseTypeDef]
    Similarity: NotRequired[float]


class ReplicationSubnetGroupTypeDef(TypedDict):
    ReplicationSubnetGroupIdentifier: NotRequired[str]
    ReplicationSubnetGroupDescription: NotRequired[str]
    VpcId: NotRequired[str]
    SubnetGroupStatus: NotRequired[str]
    Subnets: NotRequired[List[SubnetTypeDef]]
    SupportedNetworkTypes: NotRequired[List[str]]


class DescribeFleetAdvisorCollectorsResponseTypeDef(TypedDict):
    Collectors: List[CollectorResponseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateReplicationConfigResponseTypeDef(TypedDict):
    ReplicationConfig: ReplicationConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteReplicationConfigResponseTypeDef(TypedDict):
    ReplicationConfig: ReplicationConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeReplicationConfigsResponseTypeDef(TypedDict):
    Marker: str
    ReplicationConfigs: List[ReplicationConfigTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyReplicationConfigResponseTypeDef(TypedDict):
    ReplicationConfig: ReplicationConfigTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyDataMigrationMessageRequestTypeDef(TypedDict):
    DataMigrationIdentifier: str
    DataMigrationName: NotRequired[str]
    EnableCloudwatchLogs: NotRequired[bool]
    ServiceAccessRoleArn: NotRequired[str]
    DataMigrationType: NotRequired[MigrationTypeValueType]
    SourceDataSettings: NotRequired[Sequence[SourceDataSettingTypeDef]]
    NumberOfJobs: NotRequired[int]
    SelectionRules: NotRequired[str]


SourceDataSettingUnionTypeDef = Union[SourceDataSettingTypeDef, SourceDataSettingOutputTypeDef]


class CreateDataMigrationResponseTypeDef(TypedDict):
    DataMigration: DataMigrationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDataMigrationResponseTypeDef(TypedDict):
    DataMigration: DataMigrationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDataMigrationsResponseTypeDef(TypedDict):
    DataMigrations: List[DataMigrationTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyDataMigrationResponseTypeDef(TypedDict):
    DataMigration: DataMigrationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StartDataMigrationResponseTypeDef(TypedDict):
    DataMigration: DataMigrationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StopDataMigrationResponseTypeDef(TypedDict):
    DataMigration: DataMigrationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateMigrationProjectResponseTypeDef(TypedDict):
    MigrationProject: MigrationProjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteMigrationProjectResponseTypeDef(TypedDict):
    MigrationProject: MigrationProjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeMigrationProjectsResponseTypeDef(TypedDict):
    Marker: str
    MigrationProjects: List[MigrationProjectTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyMigrationProjectResponseTypeDef(TypedDict):
    MigrationProject: MigrationProjectTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateDataProviderMessageRequestTypeDef(TypedDict):
    Engine: str
    Settings: DataProviderSettingsTypeDef
    DataProviderName: NotRequired[str]
    Description: NotRequired[str]
    Tags: NotRequired[Sequence[TagTypeDef]]


class DataProviderTypeDef(TypedDict):
    DataProviderName: NotRequired[str]
    DataProviderArn: NotRequired[str]
    DataProviderCreationTime: NotRequired[datetime]
    Description: NotRequired[str]
    Engine: NotRequired[str]
    Settings: NotRequired[DataProviderSettingsTypeDef]


class ModifyDataProviderMessageRequestTypeDef(TypedDict):
    DataProviderIdentifier: str
    DataProviderName: NotRequired[str]
    Description: NotRequired[str]
    Engine: NotRequired[str]
    ExactSettings: NotRequired[bool]
    Settings: NotRequired[DataProviderSettingsTypeDef]


class DescribeFleetAdvisorDatabasesResponseTypeDef(TypedDict):
    Databases: List[DatabaseResponseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class SchemaConversionRequestTypeDef(TypedDict):
    Status: NotRequired[str]
    RequestIdentifier: NotRequired[str]
    MigrationProjectArn: NotRequired[str]
    Error: NotRequired[ErrorDetailsTypeDef]
    ExportSqlDetails: NotRequired[ExportSqlDetailsTypeDef]


class CreateEndpointResponseTypeDef(TypedDict):
    Endpoint: EndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteEndpointResponseTypeDef(TypedDict):
    Endpoint: EndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeEndpointsResponseTypeDef(TypedDict):
    Marker: str
    Endpoints: List[EndpointTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyEndpointResponseTypeDef(TypedDict):
    Endpoint: EndpointTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ApplyPendingMaintenanceActionResponseTypeDef(TypedDict):
    ResourcePendingMaintenanceActions: ResourcePendingMaintenanceActionsTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribePendingMaintenanceActionsResponseTypeDef(TypedDict):
    PendingMaintenanceActions: List[ResourcePendingMaintenanceActionsTypeDef]
    Marker: str
    ResponseMetadata: ResponseMetadataTypeDef


class RecommendationDataTypeDef(TypedDict):
    RdsEngine: NotRequired[RdsRecommendationTypeDef]


class BatchStartRecommendationsRequestRequestTypeDef(TypedDict):
    Data: NotRequired[Sequence[StartRecommendationsRequestEntryTypeDef]]


class DescribeReplicationsResponseTypeDef(TypedDict):
    Marker: str
    Replications: List[ReplicationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class StartReplicationResponseTypeDef(TypedDict):
    Replication: ReplicationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StopReplicationResponseTypeDef(TypedDict):
    Replication: ReplicationTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CancelReplicationTaskAssessmentRunResponseTypeDef(TypedDict):
    ReplicationTaskAssessmentRun: ReplicationTaskAssessmentRunTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteReplicationTaskAssessmentRunResponseTypeDef(TypedDict):
    ReplicationTaskAssessmentRun: ReplicationTaskAssessmentRunTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeReplicationTaskAssessmentRunsResponseTypeDef(TypedDict):
    Marker: str
    ReplicationTaskAssessmentRuns: List[ReplicationTaskAssessmentRunTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class StartReplicationTaskAssessmentRunResponseTypeDef(TypedDict):
    ReplicationTaskAssessmentRun: ReplicationTaskAssessmentRunTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class CreateReplicationTaskResponseTypeDef(TypedDict):
    ReplicationTask: ReplicationTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteReplicationTaskResponseTypeDef(TypedDict):
    ReplicationTask: ReplicationTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeReplicationTasksResponseTypeDef(TypedDict):
    Marker: str
    ReplicationTasks: List[ReplicationTaskTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyReplicationTaskResponseTypeDef(TypedDict):
    ReplicationTask: ReplicationTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class MoveReplicationTaskResponseTypeDef(TypedDict):
    ReplicationTask: ReplicationTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StartReplicationTaskAssessmentResponseTypeDef(TypedDict):
    ReplicationTask: ReplicationTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StartReplicationTaskResponseTypeDef(TypedDict):
    ReplicationTask: ReplicationTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class StopReplicationTaskResponseTypeDef(TypedDict):
    ReplicationTask: ReplicationTaskTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeFleetAdvisorSchemasResponseTypeDef(TypedDict):
    FleetAdvisorSchemas: List[SchemaResponseTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]


class CreateReplicationSubnetGroupResponseTypeDef(TypedDict):
    ReplicationSubnetGroup: ReplicationSubnetGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeReplicationSubnetGroupsResponseTypeDef(TypedDict):
    Marker: str
    ReplicationSubnetGroups: List[ReplicationSubnetGroupTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyReplicationSubnetGroupResponseTypeDef(TypedDict):
    ReplicationSubnetGroup: ReplicationSubnetGroupTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class ReplicationInstanceTypeDef(TypedDict):
    ReplicationInstanceIdentifier: NotRequired[str]
    ReplicationInstanceClass: NotRequired[str]
    ReplicationInstanceStatus: NotRequired[str]
    AllocatedStorage: NotRequired[int]
    InstanceCreateTime: NotRequired[datetime]
    VpcSecurityGroups: NotRequired[List[VpcSecurityGroupMembershipTypeDef]]
    AvailabilityZone: NotRequired[str]
    ReplicationSubnetGroup: NotRequired[ReplicationSubnetGroupTypeDef]
    PreferredMaintenanceWindow: NotRequired[str]
    PendingModifiedValues: NotRequired[ReplicationPendingModifiedValuesTypeDef]
    MultiAZ: NotRequired[bool]
    EngineVersion: NotRequired[str]
    AutoMinorVersionUpgrade: NotRequired[bool]
    KmsKeyId: NotRequired[str]
    ReplicationInstanceArn: NotRequired[str]
    ReplicationInstancePublicIpAddress: NotRequired[str]
    ReplicationInstancePrivateIpAddress: NotRequired[str]
    ReplicationInstancePublicIpAddresses: NotRequired[List[str]]
    ReplicationInstancePrivateIpAddresses: NotRequired[List[str]]
    ReplicationInstanceIpv6Addresses: NotRequired[List[str]]
    PubliclyAccessible: NotRequired[bool]
    SecondaryAvailabilityZone: NotRequired[str]
    FreeUntil: NotRequired[datetime]
    DnsNameServers: NotRequired[str]
    NetworkType: NotRequired[str]
    KerberosAuthenticationSettings: NotRequired[KerberosAuthenticationSettingsTypeDef]


class CreateDataMigrationMessageRequestTypeDef(TypedDict):
    MigrationProjectIdentifier: str
    DataMigrationType: MigrationTypeValueType
    ServiceAccessRoleArn: str
    DataMigrationName: NotRequired[str]
    EnableCloudwatchLogs: NotRequired[bool]
    SourceDataSettings: NotRequired[Sequence[SourceDataSettingUnionTypeDef]]
    NumberOfJobs: NotRequired[int]
    Tags: NotRequired[Sequence[TagTypeDef]]
    SelectionRules: NotRequired[str]


class CreateDataProviderResponseTypeDef(TypedDict):
    DataProvider: DataProviderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteDataProviderResponseTypeDef(TypedDict):
    DataProvider: DataProviderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeDataProvidersResponseTypeDef(TypedDict):
    Marker: str
    DataProviders: List[DataProviderTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyDataProviderResponseTypeDef(TypedDict):
    DataProvider: DataProviderTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeExtensionPackAssociationsResponseTypeDef(TypedDict):
    Marker: str
    Requests: List[SchemaConversionRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeMetadataModelAssessmentsResponseTypeDef(TypedDict):
    Marker: str
    Requests: List[SchemaConversionRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeMetadataModelConversionsResponseTypeDef(TypedDict):
    Marker: str
    Requests: List[SchemaConversionRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeMetadataModelExportsAsScriptResponseTypeDef(TypedDict):
    Marker: str
    Requests: List[SchemaConversionRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeMetadataModelExportsToTargetResponseTypeDef(TypedDict):
    Marker: str
    Requests: List[SchemaConversionRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeMetadataModelImportsResponseTypeDef(TypedDict):
    Marker: str
    Requests: List[SchemaConversionRequestTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class RecommendationTypeDef(TypedDict):
    DatabaseId: NotRequired[str]
    EngineName: NotRequired[str]
    CreatedDate: NotRequired[str]
    Status: NotRequired[str]
    Preferred: NotRequired[bool]
    Settings: NotRequired[RecommendationSettingsTypeDef]
    Data: NotRequired[RecommendationDataTypeDef]


class CreateReplicationInstanceResponseTypeDef(TypedDict):
    ReplicationInstance: ReplicationInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DeleteReplicationInstanceResponseTypeDef(TypedDict):
    ReplicationInstance: ReplicationInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeReplicationInstancesResponseTypeDef(TypedDict):
    Marker: str
    ReplicationInstances: List[ReplicationInstanceTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef


class ModifyReplicationInstanceResponseTypeDef(TypedDict):
    ReplicationInstance: ReplicationInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class RebootReplicationInstanceResponseTypeDef(TypedDict):
    ReplicationInstance: ReplicationInstanceTypeDef
    ResponseMetadata: ResponseMetadataTypeDef


class DescribeRecommendationsResponseTypeDef(TypedDict):
    Recommendations: List[RecommendationTypeDef]
    ResponseMetadata: ResponseMetadataTypeDef
    NextToken: NotRequired[str]
