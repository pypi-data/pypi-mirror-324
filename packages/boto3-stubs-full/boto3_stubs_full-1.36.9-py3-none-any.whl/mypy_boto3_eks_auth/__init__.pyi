"""
Main interface for eks-auth service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_eks_auth import (
        Client,
        EKSAuthClient,
    )

    session = Session()
    client: EKSAuthClient = session.client("eks-auth")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import EKSAuthClient

Client = EKSAuthClient

__all__ = ("Client", "EKSAuthClient")
