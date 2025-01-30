"""
Main interface for sagemaker-metrics service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_sagemaker_metrics import (
        Client,
        SageMakerMetricsClient,
    )

    session = Session()
    client: SageMakerMetricsClient = session.client("sagemaker-metrics")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import SageMakerMetricsClient

Client = SageMakerMetricsClient

__all__ = ("Client", "SageMakerMetricsClient")
