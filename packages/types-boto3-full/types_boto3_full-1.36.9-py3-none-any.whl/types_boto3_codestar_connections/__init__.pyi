"""
Main interface for codestar-connections service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_codestar_connections import (
        Client,
        CodeStarconnectionsClient,
    )

    session = Session()
    client: CodeStarconnectionsClient = session.client("codestar-connections")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import CodeStarconnectionsClient

Client = CodeStarconnectionsClient

__all__ = ("Client", "CodeStarconnectionsClient")
