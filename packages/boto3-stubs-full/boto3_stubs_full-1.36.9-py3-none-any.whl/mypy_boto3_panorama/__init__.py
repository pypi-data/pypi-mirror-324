"""
Main interface for panorama service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_panorama import (
        Client,
        PanoramaClient,
    )

    session = Session()
    client: PanoramaClient = session.client("panorama")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import PanoramaClient

Client = PanoramaClient


__all__ = ("Client", "PanoramaClient")
