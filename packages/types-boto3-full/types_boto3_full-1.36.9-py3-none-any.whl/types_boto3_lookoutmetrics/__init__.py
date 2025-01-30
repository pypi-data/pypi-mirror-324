"""
Main interface for lookoutmetrics service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_lookoutmetrics import (
        Client,
        LookoutMetricsClient,
    )

    session = Session()
    client: LookoutMetricsClient = session.client("lookoutmetrics")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import LookoutMetricsClient

Client = LookoutMetricsClient


__all__ = ("Client", "LookoutMetricsClient")
