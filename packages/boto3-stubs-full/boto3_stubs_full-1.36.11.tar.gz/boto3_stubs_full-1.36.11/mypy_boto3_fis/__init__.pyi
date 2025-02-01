"""
Main interface for fis service.

[Documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_fis/)

Copyright 2025 Vlad Emelianov

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_fis import (
        Client,
        FISClient,
    )

    session = Session()
    client: FISClient = session.client("fis")
    ```
"""

from .client import FISClient

Client = FISClient

__all__ = ("Client", "FISClient")
