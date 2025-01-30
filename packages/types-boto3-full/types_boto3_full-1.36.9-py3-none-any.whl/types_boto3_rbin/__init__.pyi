"""
Main interface for rbin service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_rbin import (
        Client,
        ListRulesPaginator,
        RecycleBinClient,
    )

    session = Session()
    client: RecycleBinClient = session.client("rbin")

    list_rules_paginator: ListRulesPaginator = client.get_paginator("list_rules")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import RecycleBinClient
from .paginator import ListRulesPaginator

Client = RecycleBinClient

__all__ = ("Client", "ListRulesPaginator", "RecycleBinClient")
