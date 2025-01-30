"""
Main interface for cloudsearch service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_cloudsearch import (
        Client,
        CloudSearchClient,
    )

    session = Session()
    client: CloudSearchClient = session.client("cloudsearch")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import CloudSearchClient

Client = CloudSearchClient

__all__ = ("Client", "CloudSearchClient")
