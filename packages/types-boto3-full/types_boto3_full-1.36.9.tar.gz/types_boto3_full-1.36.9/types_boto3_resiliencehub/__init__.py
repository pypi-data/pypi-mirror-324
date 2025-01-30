"""
Main interface for resiliencehub service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_resiliencehub import (
        Client,
        ListAppAssessmentResourceDriftsPaginator,
        ListMetricsPaginator,
        ListResourceGroupingRecommendationsPaginator,
        ResilienceHubClient,
    )

    session = Session()
    client: ResilienceHubClient = session.client("resiliencehub")

    list_app_assessment_resource_drifts_paginator: ListAppAssessmentResourceDriftsPaginator = client.get_paginator("list_app_assessment_resource_drifts")
    list_metrics_paginator: ListMetricsPaginator = client.get_paginator("list_metrics")
    list_resource_grouping_recommendations_paginator: ListResourceGroupingRecommendationsPaginator = client.get_paginator("list_resource_grouping_recommendations")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import ResilienceHubClient
from .paginator import (
    ListAppAssessmentResourceDriftsPaginator,
    ListMetricsPaginator,
    ListResourceGroupingRecommendationsPaginator,
)

Client = ResilienceHubClient


__all__ = (
    "Client",
    "ListAppAssessmentResourceDriftsPaginator",
    "ListMetricsPaginator",
    "ListResourceGroupingRecommendationsPaginator",
    "ResilienceHubClient",
)
