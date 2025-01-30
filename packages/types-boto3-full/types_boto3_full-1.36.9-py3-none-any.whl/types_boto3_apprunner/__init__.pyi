"""
Main interface for apprunner service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_apprunner import (
        AppRunnerClient,
        Client,
    )

    session = Session()
    client: AppRunnerClient = session.client("apprunner")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import AppRunnerClient

Client = AppRunnerClient

__all__ = ("AppRunnerClient", "Client")
