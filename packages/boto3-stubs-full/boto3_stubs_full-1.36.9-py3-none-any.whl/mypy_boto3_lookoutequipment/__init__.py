"""
Main interface for lookoutequipment service.

Usage::

    ```python
    from boto3.session import Session
    from mypy_boto3_lookoutequipment import (
        Client,
        LookoutEquipmentClient,
    )

    session = Session()
    client: LookoutEquipmentClient = session.client("lookoutequipment")
    ```

Copyright 2025 Vlad Emelianov
"""

from .client import LookoutEquipmentClient

Client = LookoutEquipmentClient


__all__ = ("Client", "LookoutEquipmentClient")
