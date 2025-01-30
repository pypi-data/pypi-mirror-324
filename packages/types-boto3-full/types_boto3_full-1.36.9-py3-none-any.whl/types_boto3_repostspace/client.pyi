"""
Type annotations for repostspace service Client.

[Documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/)

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_repostspace.client import RePostPrivateClient

    session = Session()
    client: RePostPrivateClient = session.client("repostspace")
    ```

Copyright 2025 Vlad Emelianov
"""

from __future__ import annotations

import sys
from typing import Any

from botocore.client import BaseClient, ClientMeta
from botocore.errorfactory import BaseClientExceptions
from botocore.exceptions import ClientError as BotocoreClientError

from .paginator import ListSpacesPaginator
from .type_defs import (
    BatchAddRoleInputRequestTypeDef,
    BatchAddRoleOutputTypeDef,
    BatchRemoveRoleInputRequestTypeDef,
    BatchRemoveRoleOutputTypeDef,
    CreateSpaceInputRequestTypeDef,
    CreateSpaceOutputTypeDef,
    DeleteSpaceInputRequestTypeDef,
    DeregisterAdminInputRequestTypeDef,
    EmptyResponseMetadataTypeDef,
    GetSpaceInputRequestTypeDef,
    GetSpaceOutputTypeDef,
    ListSpacesInputRequestTypeDef,
    ListSpacesOutputTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    RegisterAdminInputRequestTypeDef,
    SendInvitesInputRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateSpaceInputRequestTypeDef,
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

__all__ = ("RePostPrivateClient",)

class Exceptions(BaseClientExceptions):
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class RePostPrivateClient(BaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client)
    [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        RePostPrivateClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace.html#RePostPrivate.Client)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/client/can_paginate.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/#can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/client/generate_presigned_url.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/#generate_presigned_url)
        """

    def batch_add_role(
        self, **kwargs: Unpack[BatchAddRoleInputRequestTypeDef]
    ) -> BatchAddRoleOutputTypeDef:
        """
        Add role to multiple users or groups in a private re:Post.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/client/batch_add_role.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/#batch_add_role)
        """

    def batch_remove_role(
        self, **kwargs: Unpack[BatchRemoveRoleInputRequestTypeDef]
    ) -> BatchRemoveRoleOutputTypeDef:
        """
        Remove role from multiple users or groups in a private re:Post.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/client/batch_remove_role.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/#batch_remove_role)
        """

    def create_space(
        self, **kwargs: Unpack[CreateSpaceInputRequestTypeDef]
    ) -> CreateSpaceOutputTypeDef:
        """
        Creates an AWS re:Post Private private re:Post.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/client/create_space.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/#create_space)
        """

    def delete_space(
        self, **kwargs: Unpack[DeleteSpaceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an AWS re:Post Private private re:Post.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/client/delete_space.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/#delete_space)
        """

    def deregister_admin(
        self, **kwargs: Unpack[DeregisterAdminInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes the user or group from the list of administrators of the private
        re:Post.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/client/deregister_admin.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/#deregister_admin)
        """

    def get_space(self, **kwargs: Unpack[GetSpaceInputRequestTypeDef]) -> GetSpaceOutputTypeDef:
        """
        Displays information about the AWS re:Post Private private re:Post.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/client/get_space.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/#get_space)
        """

    def list_spaces(
        self, **kwargs: Unpack[ListSpacesInputRequestTypeDef]
    ) -> ListSpacesOutputTypeDef:
        """
        Returns a list of AWS re:Post Private private re:Posts in the account with some
        information about each private re:Post.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/client/list_spaces.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/#list_spaces)
        """

    def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns the tags that are associated with the AWS re:Post Private resource
        specified by the resourceArn.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/client/list_tags_for_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/#list_tags_for_resource)
        """

    def register_admin(
        self, **kwargs: Unpack[RegisterAdminInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Adds a user or group to the list of administrators of the private re:Post.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/client/register_admin.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/#register_admin)
        """

    def send_invites(
        self, **kwargs: Unpack[SendInvitesInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Sends an invitation email to selected users and groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/client/send_invites.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/#send_invites)
        """

    def tag_resource(self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]) -> Dict[str, Any]:
        """
        Associates tags with an AWS re:Post Private resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/client/tag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/#tag_resource)
        """

    def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes the association of the tag with the AWS re:Post Private resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/client/untag_resource.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/#untag_resource)
        """

    def update_space(
        self, **kwargs: Unpack[UpdateSpaceInputRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Modifies an existing AWS re:Post Private private re:Post.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/client/update_space.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/#update_space)
        """

    def get_paginator(  # type: ignore[override]
        self, operation_name: Literal["list_spaces"]
    ) -> ListSpacesPaginator:
        """
        Create a paginator for an operation.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/repostspace/client/get_paginator.html)
        [Show types-boto3-full documentation](https://youtype.github.io/types_boto3_docs/types_boto3_repostspace/client/#get_paginator)
        """
