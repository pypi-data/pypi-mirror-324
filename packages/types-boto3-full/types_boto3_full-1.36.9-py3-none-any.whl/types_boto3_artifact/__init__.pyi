"""
Main interface for artifact service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_artifact import (
        ArtifactClient,
        Client,
        ListCustomerAgreementsPaginator,
        ListReportsPaginator,
    )

    session = Session()
    client: ArtifactClient = session.client("artifact")

    list_customer_agreements_paginator: ListCustomerAgreementsPaginator = client.get_paginator("list_customer_agreements")
    list_reports_paginator: ListReportsPaginator = client.get_paginator("list_reports")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import ArtifactClient
from .paginator import ListCustomerAgreementsPaginator, ListReportsPaginator

Client = ArtifactClient

__all__ = ("ArtifactClient", "Client", "ListCustomerAgreementsPaginator", "ListReportsPaginator")
