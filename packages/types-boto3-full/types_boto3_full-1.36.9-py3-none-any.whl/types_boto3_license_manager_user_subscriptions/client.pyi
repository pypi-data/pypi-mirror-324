"""
Type annotations for license-manager-user-subscriptions service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_license_manager_user_subscriptions.client import LicenseManagerUserSubscriptionsClient

    session = Session()
    client: LicenseManagerUserSubscriptionsClient = session.client("license-manager-user-subscriptions")
    ```

Copyright 2025 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Any, overload

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import (
    ListIdentityProvidersPaginator,
    ListInstancesPaginator,
    ListLicenseServerEndpointsPaginator,
    ListProductSubscriptionsPaginator,
    ListUserAssociationsPaginator,
)
from .type_defs import (
    AssociateUserRequestRequestTypeDef,
    AssociateUserResponseTypeDef,
    CreateLicenseServerEndpointRequestRequestTypeDef,
    CreateLicenseServerEndpointResponseTypeDef,
    DeleteLicenseServerEndpointRequestRequestTypeDef,
    DeleteLicenseServerEndpointResponseTypeDef,
    DeregisterIdentityProviderRequestRequestTypeDef,
    DeregisterIdentityProviderResponseTypeDef,
    DisassociateUserRequestRequestTypeDef,
    DisassociateUserResponseTypeDef,
    ListIdentityProvidersRequestRequestTypeDef,
    ListIdentityProvidersResponseTypeDef,
    ListInstancesRequestRequestTypeDef,
    ListInstancesResponseTypeDef,
    ListLicenseServerEndpointsRequestRequestTypeDef,
    ListLicenseServerEndpointsResponseTypeDef,
    ListProductSubscriptionsRequestRequestTypeDef,
    ListProductSubscriptionsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListUserAssociationsRequestRequestTypeDef,
    ListUserAssociationsResponseTypeDef,
    RegisterIdentityProviderRequestRequestTypeDef,
    RegisterIdentityProviderResponseTypeDef,
    StartProductSubscriptionRequestRequestTypeDef,
    StartProductSubscriptionResponseTypeDef,
    StopProductSubscriptionRequestRequestTypeDef,
    StopProductSubscriptionResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateIdentityProviderSettingsRequestRequestTypeDef,
    UpdateIdentityProviderSettingsResponseTypeDef,
)

if sys.version_info >= (3, 9):
    from builtins import dict as Dict
    from builtins import type as Type
    from collections.abc import Mapping
else:
    from typing import Dict, Mapping, Type
if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("LicenseManagerUserSubscriptionsClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class LicenseManagerUserSubscriptionsClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions.html#LicenseManagerUserSubscriptions.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        LicenseManagerUserSubscriptionsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions.html#LicenseManagerUserSubscriptions.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#generate_presigned_url)
        """

    def associate_user(
        self, **kwargs: Unpack[AssociateUserRequestRequestTypeDef]
    ) -> AssociateUserResponseTypeDef:
        """
        Associates the user to an EC2 instance to utilize user-based subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/associate_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#associate_user)
        """

    def create_license_server_endpoint(
        self, **kwargs: Unpack[CreateLicenseServerEndpointRequestRequestTypeDef]
    ) -> CreateLicenseServerEndpointResponseTypeDef:
        """
        Creates a network endpoint for the Remote Desktop Services (RDS) license server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/create_license_server_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#create_license_server_endpoint)
        """

    def delete_license_server_endpoint(
        self, **kwargs: Unpack[DeleteLicenseServerEndpointRequestRequestTypeDef]
    ) -> DeleteLicenseServerEndpointResponseTypeDef:
        """
        Deletes a <code>LicenseServerEndpoint</code> resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/delete_license_server_endpoint.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#delete_license_server_endpoint)
        """

    def deregister_identity_provider(
        self, **kwargs: Unpack[DeregisterIdentityProviderRequestRequestTypeDef]
    ) -> DeregisterIdentityProviderResponseTypeDef:
        """
        Deregisters the Active Directory identity provider from License Manager
        user-based subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/deregister_identity_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#deregister_identity_provider)
        """

    def disassociate_user(
        self, **kwargs: Unpack[DisassociateUserRequestRequestTypeDef]
    ) -> DisassociateUserResponseTypeDef:
        """
        Disassociates the user from an EC2 instance providing user-based subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/disassociate_user.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#disassociate_user)
        """

    def list_identity_providers(
        self, **kwargs: Unpack[ListIdentityProvidersRequestRequestTypeDef]
    ) -> ListIdentityProvidersResponseTypeDef:
        """
        Lists the Active Directory identity providers for user-based subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/list_identity_providers.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#list_identity_providers)
        """

    def list_instances(
        self, **kwargs: Unpack[ListInstancesRequestRequestTypeDef]
    ) -> ListInstancesResponseTypeDef:
        """
        Lists the EC2 instances providing user-based subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/list_instances.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#list_instances)
        """

    def list_license_server_endpoints(
        self, **kwargs: Unpack[ListLicenseServerEndpointsRequestRequestTypeDef]
    ) -> ListLicenseServerEndpointsResponseTypeDef:
        """
        List the Remote Desktop Services (RDS) License Server endpoints.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/list_license_server_endpoints.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#list_license_server_endpoints)
        """

    def list_product_subscriptions(
        self, **kwargs: Unpack[ListProductSubscriptionsRequestRequestTypeDef]
    ) -> ListProductSubscriptionsResponseTypeDef:
        """
        Lists the user-based subscription products available from an identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/list_product_subscriptions.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#list_product_subscriptions)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns the list of tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#list_tags_for_resource)
        """

    def list_user_associations(
        self, **kwargs: Unpack[ListUserAssociationsRequestRequestTypeDef]
    ) -> ListUserAssociationsResponseTypeDef:
        """
        Lists user associations for an identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/list_user_associations.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#list_user_associations)
        """

    def register_identity_provider(
        self, **kwargs: Unpack[RegisterIdentityProviderRequestRequestTypeDef]
    ) -> RegisterIdentityProviderResponseTypeDef:
        """
        Registers an identity provider for user-based subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/register_identity_provider.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#register_identity_provider)
        """

    def start_product_subscription(
        self, **kwargs: Unpack[StartProductSubscriptionRequestRequestTypeDef]
    ) -> StartProductSubscriptionResponseTypeDef:
        """
        Starts a product subscription for a user with the specified identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/start_product_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#start_product_subscription)
        """

    def stop_product_subscription(
        self, **kwargs: Unpack[StopProductSubscriptionRequestRequestTypeDef]
    ) -> StopProductSubscriptionResponseTypeDef:
        """
        Stops a product subscription for a user with the specified identity provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/stop_product_subscription.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#stop_product_subscription)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Adds tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#untag_resource)
        """

    def update_identity_provider_settings(
        self, **kwargs: Unpack[UpdateIdentityProviderSettingsRequestRequestTypeDef]
    ) -> UpdateIdentityProviderSettingsResponseTypeDef:
        """
        Updates additional product configuration settings for the registered identity
        provider.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/update_identity_provider_settings.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#update_identity_provider_settings)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_identity_providers"]
    ) -> ListIdentityProvidersPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_instances"]
    ) -> ListInstancesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_license_server_endpoints"]
    ) -> ListLicenseServerEndpointsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_product_subscriptions"]
    ) -> ListProductSubscriptionsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#get_paginator)
        """

    @overload  # type: ignore[override]
    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_user_associations"]
    ) -> ListUserAssociationsPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/license-manager-user-subscriptions/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_license_manager_user_subscriptions/client/#get_paginator)
        """
