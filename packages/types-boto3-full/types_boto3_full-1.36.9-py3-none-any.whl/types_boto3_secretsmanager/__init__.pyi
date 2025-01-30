"""
Main interface for secretsmanager service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_secretsmanager import (
        Client,
        ListSecretsPaginator,
        SecretsManagerClient,
    )

    session = Session()
    client: SecretsManagerClient = session.client("secretsmanager")

    list_secrets_paginator: ListSecretsPaginator = client.get_paginator("list_secrets")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import SecretsManagerClient
from .paginator import ListSecretsPaginator

Client = SecretsManagerClient

__all__ = ("Client", "ListSecretsPaginator", "SecretsManagerClient")
