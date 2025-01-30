"""
Main interface for cognito-identity service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_cognito_identity import (
        Client,
        CognitoIdentityClient,
        ListIdentityPoolsPaginator,
    )

    session = Session()
    client: CognitoIdentityClient = session.client("cognito-identity")

    list_identity_pools_paginator: ListIdentityPoolsPaginator = client.get_paginator("list_identity_pools")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import CognitoIdentityClient
from .paginator import ListIdentityPoolsPaginator

Client = CognitoIdentityClient

__all__ = ("Client", "CognitoIdentityClient", "ListIdentityPoolsPaginator")
