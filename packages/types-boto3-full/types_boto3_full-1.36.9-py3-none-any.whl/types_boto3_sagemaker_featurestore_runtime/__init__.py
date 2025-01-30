"""
Main interface for sagemaker-featurestore-runtime service.

Usage::

    ```python
    from boto3.session import Session
    from types_boto3_sagemaker_featurestore_runtime import (
        Client,
        SageMakerFeatureStoreRuntimeClient,
    )

    session = Session()
    client: SageMakerFeatureStoreRuntimeClient = session.client("sagemaker-featurestore-runtime")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import SageMakerFeatureStoreRuntimeClient

Client = SageMakerFeatureStoreRuntimeClient


__all__ = ("Client", "SageMakerFeatureStoreRuntimeClient")
