"""
Type annotations for s3tables service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_s3tables.client import S3TablesClient

    session = Session()
    client: S3TablesClient = session.client("s3tables")
    ```

Copyright 2025 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListNamespacesPaginator, ListTableBucketsPaginator, ListTablesPaginator
from .type_defs import (
    CreateNamespaceRequestRequestTypeDef,
    CreateNamespaceResponseTypeDef,
    CreateTableBucketRequestRequestTypeDef,
    CreateTableBucketResponseTypeDef,
    CreateTableRequestRequestTypeDef,
    CreateTableResponseTypeDef,
    DeleteNamespaceRequestRequestTypeDef,
    DeleteTableBucketPolicyRequestRequestTypeDef,
    DeleteTableBucketRequestRequestTypeDef,
    DeleteTablePolicyRequestRequestTypeDef,
    DeleteTableRequestRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetNamespaceRequestRequestTypeDef,
    GetNamespaceResponseTypeDef,
    GetTableBucketMaintenanceConfigurationRequestRequestTypeDef,
    GetTableBucketMaintenanceConfigurationResponseTypeDef,
    GetTableBucketPolicyRequestRequestTypeDef,
    GetTableBucketPolicyResponseTypeDef,
    GetTableBucketRequestRequestTypeDef,
    GetTableBucketResponseTypeDef,
    GetTableMaintenanceConfigurationRequestRequestTypeDef,
    GetTableMaintenanceConfigurationResponseTypeDef,
    GetTableMaintenanceJobStatusRequestRequestTypeDef,
    GetTableMaintenanceJobStatusResponseTypeDef,
    GetTableMetadataLocationRequestRequestTypeDef,
    GetTableMetadataLocationResponseTypeDef,
    GetTablePolicyRequestRequestTypeDef,
    GetTablePolicyResponseTypeDef,
    GetTableRequestRequestTypeDef,
    GetTableResponseTypeDef,
    ListNamespacesRequestRequestTypeDef,
    ListNamespacesResponseTypeDef,
    ListTableBucketsRequestRequestTypeDef,
    ListTableBucketsResponseTypeDef,
    ListTablesRequestRequestTypeDef,
    ListTablesResponseTypeDef,
    PutTableBucketMaintenanceConfigurationRequestRequestTypeDef,
    PutTableBucketPolicyRequestRequestTypeDef,
    PutTableMaintenanceConfigurationRequestRequestTypeDef,
    PutTablePolicyRequestRequestTypeDef,
    RenameTableRequestRequestTypeDef,
    UpdateTableMetadataLocationRequestRequestTypeDef,
    UpdateTableMetadataLocationResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("S3TablesClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    BadRequestException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    ForbiddenException: Type[BotocoreClientError]
    InternalServerErrorException: Type[BotocoreClientError]
    NotFoundException: Type[BotocoreClientError]
    TooManyRequestsException: Type[BotocoreClientError]

class S3TablesClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables.html#S3Tables.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        S3TablesClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables.html#S3Tables.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#generate_presigned_url)
        """

    def create_namespace(
        self, **kwargs: Unpack[CreateNamespaceRequestRequestTypeDef]
    ) -> CreateNamespaceResponseTypeDef:
        """
        Creates a namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/create_namespace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#create_namespace)
        """

    def create_table(
        self, **kwargs: Unpack[CreateTableRequestRequestTypeDef]
    ) -> CreateTableResponseTypeDef:
        """
        Creates a new table associated with the given namespace in a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/create_table.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#create_table)
        """

    def create_table_bucket(
        self, **kwargs: Unpack[CreateTableBucketRequestRequestTypeDef]
    ) -> CreateTableBucketResponseTypeDef:
        """
        Creates a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/create_table_bucket.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#create_table_bucket)
        """

    def delete_namespace(
        self, **kwargs: Unpack[DeleteNamespaceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/delete_namespace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#delete_namespace)
        """

    def delete_table(
        self, **kwargs: Unpack[DeleteTableRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/delete_table.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#delete_table)
        """

    def delete_table_bucket(
        self, **kwargs: Unpack[DeleteTableBucketRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/delete_table_bucket.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#delete_table_bucket)
        """

    def delete_table_bucket_policy(
        self, **kwargs: Unpack[DeleteTableBucketPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a table bucket policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/delete_table_bucket_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#delete_table_bucket_policy)
        """

    def delete_table_policy(
        self, **kwargs: Unpack[DeleteTablePolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a table policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/delete_table_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#delete_table_policy)
        """

    def get_namespace(
        self, **kwargs: Unpack[GetNamespaceRequestRequestTypeDef]
    ) -> GetNamespaceResponseTypeDef:
        """
        Gets details about a namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_namespace.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#get_namespace)
        """

    def get_table(self, **kwargs: Unpack[GetTableRequestRequestTypeDef]) -> GetTableResponseTypeDef:
        """
        Gets details about a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#get_table)
        """

    def get_table_bucket(
        self, **kwargs: Unpack[GetTableBucketRequestRequestTypeDef]
    ) -> GetTableBucketResponseTypeDef:
        """
        Gets details on a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_bucket.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#get_table_bucket)
        """

    def get_table_bucket_maintenance_configuration(
        self, **kwargs: Unpack[GetTableBucketMaintenanceConfigurationRequestRequestTypeDef]
    ) -> GetTableBucketMaintenanceConfigurationResponseTypeDef:
        """
        Gets details about a maintenance configuration for a given table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_bucket_maintenance_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#get_table_bucket_maintenance_configuration)
        """

    def get_table_bucket_policy(
        self, **kwargs: Unpack[GetTableBucketPolicyRequestRequestTypeDef]
    ) -> GetTableBucketPolicyResponseTypeDef:
        """
        Gets details about a table bucket policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_bucket_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#get_table_bucket_policy)
        """

    def get_table_maintenance_configuration(
        self, **kwargs: Unpack[GetTableMaintenanceConfigurationRequestRequestTypeDef]
    ) -> GetTableMaintenanceConfigurationResponseTypeDef:
        """
        Gets details about the maintenance configuration of a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_maintenance_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#get_table_maintenance_configuration)
        """

    def get_table_maintenance_job_status(
        self, **kwargs: Unpack[GetTableMaintenanceJobStatusRequestRequestTypeDef]
    ) -> GetTableMaintenanceJobStatusResponseTypeDef:
        """
        Gets the status of a maintenance job for a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_maintenance_job_status.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#get_table_maintenance_job_status)
        """

    def get_table_metadata_location(
        self, **kwargs: Unpack[GetTableMetadataLocationRequestRequestTypeDef]
    ) -> GetTableMetadataLocationResponseTypeDef:
        """
        Gets the location of the table metadata.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_metadata_location.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#get_table_metadata_location)
        """

    def get_table_policy(
        self, **kwargs: Unpack[GetTablePolicyRequestRequestTypeDef]
    ) -> GetTablePolicyResponseTypeDef:
        """
        Gets details about a table policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_table_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#get_table_policy)
        """

    def list_namespaces(
        self, **kwargs: Unpack[ListNamespacesRequestRequestTypeDef]
    ) -> ListNamespacesResponseTypeDef:
        """
        Lists the namespaces within a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/list_namespaces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#list_namespaces)
        """

    def list_table_buckets(
        self, **kwargs: Unpack[ListTableBucketsRequestRequestTypeDef]
    ) -> ListTableBucketsResponseTypeDef:
        """
        Lists table buckets for your account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/list_table_buckets.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#list_table_buckets)
        """

    def list_tables(
        self, **kwargs: Unpack[ListTablesRequestRequestTypeDef]
    ) -> ListTablesResponseTypeDef:
        """
        List tables in the given table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/list_tables.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#list_tables)
        """

    def put_table_bucket_maintenance_configuration(
        self, **kwargs: Unpack[PutTableBucketMaintenanceConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a new maintenance configuration or replaces an existing maintenance
        configuration for a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/put_table_bucket_maintenance_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#put_table_bucket_maintenance_configuration)
        """

    def put_table_bucket_policy(
        self, **kwargs: Unpack[PutTableBucketPolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a new maintenance configuration or replaces an existing table bucket
        policy for a table bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/put_table_bucket_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#put_table_bucket_policy)
        """

    def put_table_maintenance_configuration(
        self, **kwargs: Unpack[PutTableMaintenanceConfigurationRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a new maintenance configuration or replaces an existing maintenance
        configuration for a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/put_table_maintenance_configuration.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#put_table_maintenance_configuration)
        """

    def put_table_policy(
        self, **kwargs: Unpack[PutTablePolicyRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Creates a new maintenance configuration or replaces an existing table policy
        for a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/put_table_policy.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#put_table_policy)
        """

    def rename_table(
        self, **kwargs: Unpack[RenameTableRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Renames a table or a namespace.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/rename_table.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#rename_table)
        """

    def update_table_metadata_location(
        self, **kwargs: Unpack[UpdateTableMetadataLocationRequestRequestTypeDef]
    ) -> UpdateTableMetadataLocationResponseTypeDef:
        """
        Updates the metadata location for a table.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/update_table_metadata_location.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#update_table_metadata_location)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_namespaces"]
    ) -> ListNamespacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_table_buckets"]
    ) -> ListTableBucketsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_tables"]
    ) -> ListTablesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3tables/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_s3tables/client/#get_paginator)
        """
