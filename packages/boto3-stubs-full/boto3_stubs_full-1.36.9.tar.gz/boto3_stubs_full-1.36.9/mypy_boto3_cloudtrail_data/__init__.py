"""
Main interface for cloudtrail-data service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cloudtrail_data import (
        Client,
        CloudTrailDataServiceClient,
    )

    session = Session()
    client: CloudTrailDataServiceClient = session.client("cloudtrail-data")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import CloudTrailDataServiceClient

Client = CloudTrailDataServiceClient


__all__ = ("Client", "CloudTrailDataServiceClient")
